import asyncio

import pandas as pd
from sklearn.linear_model import LinearRegression
from checker.binance_handler import BinanceGetDate
from checker.unix_time import convert_date_to_unix_time_by_string


async def main():
    pass


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        # data for train model
        self.eth_btc_data = pd.DataFrame()

    async def load_eth_btc_data(self, from_date, to_date, ):
        pass

    async def calculate_price_movements(self):
        self.eth_btc_data['ETHUSDT_price_movements'] =\
            self.eth_btc_data['ETHUSDT'].diff() / self.eth_btc_data['ETHUSDT'].shift(1)
        self.eth_btc_data.dropna(inplace=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
