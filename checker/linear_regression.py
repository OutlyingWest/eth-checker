import asyncio
import pandas as pd
from sklearn.linear_model import LinearRegression


async def main():
    pass


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        # data for train model
        self.eth_btc_frame = pd.DataFrame()

    def calculate_price_movements(self):
        self.eth_btc_frame['ETHUSDT_price_movements'] = \
            self.eth_btc_frame['ETHUSDT'].diff() / self.eth_btc_frame['ETHUSDT'].shift(1)
        self.eth_btc_frame.dropna(inplace=True)

    async def train_model(self):
        """ Train the regression model """
        self.calculate_price_movements()
        self.eth_btc_frame['ETHUSDT'] = self.eth_btc_frame['ETHUSDT']
        trane_data = self.eth_btc_frame[['ETHUSDT', 'BTCUSDT']]
        target_values = self.eth_btc_frame['ETHUSDT_price_movements']
        self.model = LinearRegression().fit(trane_data, target_values)
        # print(self.eth_btc_frame[['ETHUSDT', 'close_time']])
        print(self.eth_btc_frame)
        print('Updating of history data complete!')

    def get_eth_btc_frame(self, frame):
        self.eth_btc_frame = frame


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
