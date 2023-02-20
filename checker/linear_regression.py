"""
Contains class to interaction with linear regression model.
"""
import pandas as pd
from sklearn.linear_model import LinearRegression


class LinearRegressionModel:
    """
    Class which contains LinearRegression() instance
    and allow to load data for train it.
    """
    def __init__(self):
        self.model = LinearRegression()
        # data for train model
        self.eth_btc_frame = None

    async def train_model(self):
        """ Train the regression model """
        trane_data = self.eth_btc_frame[['BTCUSDT']]
        target_values = self.eth_btc_frame['ETHUSDT']
        self.model = LinearRegression().fit(trane_data, target_values)
        print(self.eth_btc_frame[['BTCUSDT', 'ETHUSDT']])
        print('Updating of history data complete!')

    def put_eth_btc_frame(self, frame: pd.DataFrame):
        self.eth_btc_frame = frame
