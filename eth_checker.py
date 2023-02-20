"""
Program entry point module.
"""
import asyncio
import pandas as pd
from checker.configuration import load_config
from checker.linear_regression import LinearRegressionModel, LinearRegression
from checker.time_manager import convert_date_to_unix_time_by_string, time_to_seconds, ResponseTimer
from checker.binance_handler import HistoryDataManager, BinanceGetDate


async def main():
    """
    Creates and executes all tasks asynchronously.
    - Allows to set the start and end dates of collecting historical data for training. Format Y-m-d
    - Allows to set the period of updating historical data. Format: integer.
    - Allows to set sample of getting historical data from Binance. Format: 1m, 3h, 2d, 1M
    """
    # Instance to perform linear regression
    model = LinearRegressionModel()
    # Instance to get data about ETHUSDT, BTCUSDT pairs from Binance
    binance = BinanceGetDate()
    # Load settings from config.txt
    config = load_config('config.txt')
    # Set dates to define period of loading historical data on currency pairs
    initial_from_date = convert_date_to_unix_time_by_string(config.from_date)
    initial_to_date = convert_date_to_unix_time_by_string(config.to_date)
    # Set how often historical data needs to update
    update_period = time_to_seconds(minutes=config.update_period)
    # Set sample of getting data from Binance
    sample_time = config.sample_time
    # Tasks for asynchronous execution
    tasks = [
        train_eth_btc_model(model, initial_from_date, initial_to_date, update_period, sample_time=sample_time),
        binance.get_stream_of_pairs_data(['btcusdt', 'ethusdt']),
        check_eth_course(binance, model, print_detailed_info=config.print_detailed_info),
    ]
    await asyncio.gather(*tasks)


async def train_eth_btc_model(linear_model: LinearRegressionModel, from_date, to_date,
                              update_period: int, sample_time: str):
    """
    Retrain model with an actual ETHUSDT, BTCUSDT pairs data.
    :param linear_model: LinearRegressionModel() class object.
    :param from_date: (unix) defines initial start date of getting from binance.
    :param to_date: (unix) defines initial stop date of getting from binance.
    :param update_period: how often model will update.
    :param sample_time: how often will the data be sampled. For example: 1m, 1h, 1d, 1M.
    """
    manager = HistoryDataManager(from_date, to_date,
                                 update_period=update_period,
                                 sample_time=sample_time)
    while True:
        await manager.update_eth_btc_history_frame()
        eth_btc_history_frame = await manager.eth_btc_history_frame.get()
        linear_model.put_eth_btc_frame(eth_btc_history_frame)
        await linear_model.train_model()
        await asyncio.sleep(update_period)


async def check_eth_course(binance: BinanceGetDate, linear_regression: LinearRegressionModel,
                           print_detailed_info=False):
    """
    This task monitors the price of the futures and, using the linear regression method,
    determines its own movements in the price of ETH. If the price changes by 1% in the last 60 minutes,
    the task prints a message to the console.
    :param binance: LinearRegressionModel() class object.
    :param linear_regression: (unix) defines initial start date of getting from binance.
    :param print_detailed_info: Allow to print information about ETHUSDT, BTCUSDT current prices,
                                ETHUSDT predicted price and price changes.
    """
    # Сreation of a timer object that determines the frequency of sending messages about exceeding the price
    response_timer = ResponseTimer()
    # Response to change price over 1% period
    response_timeout = time_to_seconds(minutes=60)
    asyncio.create_task(response_timer.run(timeout=response_timeout))
    while True:
        # Get the current ETHUSDT and BTCUSDT prices
        current_eth_price = await binance.get_price_from_eth_queue()
        current_btc_price = await binance.get_price_from_btc_queue()

        # Use the trained model to predict the movement of the ETHUSDT price
        if linear_regression.model:
            linear_regression_model: LinearRegression = linear_regression.model
            eth_movement_prediction = linear_regression_model.predict(pd.DataFrame({'BTCUSDT': [current_btc_price]}))

            # Check if the price has changed by 1% in the last 60 minutes
            is_price_changed = False
            last_exceeded_eth_price = None
            price_change = abs(eth_movement_prediction[0] - current_eth_price) / current_eth_price
            if print_detailed_info:
                print(f'ETHUSDT prices: Predicted:{eth_movement_prediction[0]:.2f} Current:{current_eth_price:.2f} '
                      f'Price change:{price_change:.2f} '
                      f'BTCUSDT price current:{current_btc_price}')
            if price_change >= 0.01:
                is_price_changed = True
                last_exceeded_eth_price = current_eth_price
            # Check is time to print response out
            is_timeout_passed = response_timer.check_timer()
            if is_timeout_passed and is_price_changed:
                await response_timer.restart()
                print('The ETHUSDT price has changed by 1% in the last 60 minutes. ' +
                      f'Last ETHUSDT price:{last_exceeded_eth_price}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
