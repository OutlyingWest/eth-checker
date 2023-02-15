import asyncio
from checker.binance_handler import DataManager
from checker.linear_regression import LinearRegressionModel
from checker.unix_time import convert_date_to_unix_time_by_string


async def main():
    model = LinearRegressionModel()
    from_date = convert_date_to_unix_time_by_string('2022-1-15')
    to_date = convert_date_to_unix_time_by_string('2023-2-15')
    update_period = 6
    tasks = [
        train_eth_btc_model(model, from_date, to_date, update_period, sample_time='1d'),
    ]
    await asyncio.gather(*tasks)


async def train_eth_btc_model(linear_model, from_date, to_date, update_period, sample_time: str):
    """ Load historical data for ETHUSDT and BTCUSDT prices """
    manager = DataManager(from_date, to_date,
                          update_period=update_period,
                          sample_time=sample_time)
    while True:
        await manager.update_eth_btc_history_frame()
        linear_model.eth_btc_data = await manager.eth_btc_history_frame.get()
        linear_model.train_model()
        await asyncio.sleep(update_period)
    # await manager.binance.session.close()


async def check_eth_course():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
