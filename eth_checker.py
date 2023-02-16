import asyncio
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from checker.linear_regression import LinearRegressionModel, LinearRegression
from checker.unix_time import convert_date_to_unix_time_by_string, time_to_seconds, ResponseTimer
from checker.binance_handler import HistoryDataManager, BinanceGetDate


async def main():
    model = LinearRegressionModel()
    binance = BinanceGetDate()
    # Sets dates for loading historical data on currency pairs
    initial_from_date = convert_date_to_unix_time_by_string('2023-1-15')
    initial_to_date = convert_date_to_unix_time_by_string('2023-2-15')
    # Set how often historical data needs to update
    update_period = 15  # time_to_seconds()
    # Tasks for asynchronous execution
    tasks = [
        train_eth_btc_model(model, initial_from_date, initial_to_date, update_period, sample_time='1m'),
        binance.get_stream_of_pairs_data(['btcusdt', 'ethusdt']),
        check_eth_course(binance, model),
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
        linear_model.get_eth_btc_frame(eth_btc_history_frame)
        await linear_model.train_model()
        # await plotter(eth_btc_history_frame)
        await asyncio.sleep(update_period)


async def check_eth_course(binance: BinanceGetDate, linear_regression: LinearRegressionModel):
    """
    This task monitors the price of the futures and, using the linear regression method,
    determines its own movements in the price of ETH. If the price changes by 1% in the last 60 minutes,
    the task prints a message to the console.
    :param binance: LinearRegressionModel() class object.
    :param linear_regression: (unix) defines initial start date of getting from binance.
    """
    # response_timer_task = asyncio.create_task(response_timer(10))
    response_timer = ResponseTimer()
    asyncio.create_task(response_timer.run(timeout=10))
    while True:
        # Get the current ETHUSDT and BTCUSDT prices
        current_eth_price = await binance.get_price_from_eth_queue()
        current_btc_price = await binance.get_price_from_btc_queue()
        print('ETHUSDT:', current_eth_price)
        print('BTCUSDT:', current_btc_price)

        # Use the trained model to predict the movement of the ETHUSDT price
        if linear_regression.model:
            linear_regression_model: LinearRegression = linear_regression.model
            eth_movement_prediction = linear_regression_model.predict(pd.DataFrame({'ETHUSDT': [current_eth_price],
                                                                                    'BTCUSDT': [current_btc_price]}))

            # Check if the price has changed by 1% in the last 60 minutes
            is_price_changed = False
            last_exceeded_eth_price = None
            price_change = abs(eth_movement_prediction[0] - current_eth_price) / current_eth_price
            # print('price change:', price_change, 'eth_movement_prediction[0]:', eth_movement_prediction[0],
            #       'current_eth_price:', current_eth_price)
            if price_change >= 0.01:
                is_price_changed = True
                last_exceeded_eth_price = current_eth_price
            # Check is time to print response out
            is_timeout_passed = response_timer.check_timer()
            if is_timeout_passed and is_price_changed:
                await response_timer.restart()
                print('The ETHUSDT price has changed by 1% in the last 60 minutes. ' +
                      f'Last ETHUSDT price:{last_exceeded_eth_price}')







async def plotter(data_frame: pd.DataFrame):
    mpl.use('TkAgg')  # !IMPORTANT
    # plot the data
    fig, ax = plt.subplots()
    ax.plot(data_frame['close_time'], data_frame['ETHUSDT'])
    ax.plot(data_frame['close_time'], data_frame['BTCUSDT'])
    ax.legend(labels=('ETHUSDT', 'BTCUSDT'))
    # add labels and title
    plt.xlabel('time')
    plt.ylabel('crypto')
    plt.title('Cypto Plot')
    # show the plot
    plt.show()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
