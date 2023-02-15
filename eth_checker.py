import asyncio
from checker.linear_regression import LinearRegressionModel
from checker.unix_time import convert_date_to_unix_time_by_string
from checker.binance_handler import HistoryDataManager, BinanceGetDate


async def main():
    model = LinearRegressionModel()
    binance = BinanceGetDate()
    initial_from_date = convert_date_to_unix_time_by_string('2022-1-15')
    initial_to_date = convert_date_to_unix_time_by_string('2023-2-15')
    update_period = 6
    tasks = [
        train_eth_btc_model(model, initial_from_date, initial_to_date, update_period, sample_time='1d'),
        binance.get_stream_recent_pairs_data(['btcusdt', 'ethusdt']),
        get_eth_queue(binance),
        get_btc_queue(binance),
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
        linear_model.eth_btc_data = await manager.eth_btc_history_frame.get()
        linear_model.train_model()
        await asyncio.sleep(update_period)
    # await manager.binance.session.close()


async def get_eth_queue(binance: BinanceGetDate):
    while True:
        print('I take eth queue:', await binance.eth_price_queue.get())


async def get_btc_queue(binance: BinanceGetDate):
    while True:
        print('I take btc queue:', await binance.btc_price_queue.get())


async def check_eth_course():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
