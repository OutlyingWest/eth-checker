import aiohttp
import asyncio
import json
import pandas as pd
from pprint import pprint
from checker.unix_time import convert_date_to_unix_time_by_string


async def main():
    pass


class BinanceGetDate:
    """
    Allow to get data about ETHUSDT, BTCUSDT pairs for a period
    and save it to dataframe
    """
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.pairs = {}
        self.eth_btc_history_frame = pd.DataFrame()

    async def load_pair_history(self, pair: str, from_date: int, to_date: int, interval='1d'):
        """ Returns pair history in json object """
        async with self.session.get(
                f'https://api.binance.com/api/v3/klines?' +
                f'symbol={pair}&interval={interval}&startTime={from_date}&endTime={to_date}'
        ) as response:
            klines_byte_string = await response.read()
            json_klines = json.loads(klines_byte_string)
            pair_dict = {pair: json_klines}
            self.pairs.update(pair_dict)
            return pair_dict

    @staticmethod
    async def make_pair_history_data_frame(pair_histories):
        pair_frames = []
        for pair_history in pair_histories:
            for pair_name, pair_history_value in pair_history.items():
                pair_close_price_col = [float(pair_history_kline[4]) for pair_history_kline in pair_history_value]
                if pair_name == 'BTCUSDT':
                    pair_close_time_col = [int(pair_history_kline[6]) for pair_history_kline in pair_history_value]
                    pair_frames.append(pd.DataFrame({pair_name: pair_close_price_col,
                                                     'close_time': pair_close_time_col}))
                else:
                    pair_frames.append(pd.DataFrame({pair_name: pair_close_price_col}))

        eth_btc_pair_histories = pd.concat(pair_frames, axis=1)
        return eth_btc_pair_histories

    async def load_pairs_history_frame(self, from_date, to_date, interval='1d'):
        """
        Load data about ETHUSDT, BTCUSDT and close price time for a period
        :param from_date: (unix) defines initial start date of getting from binance.
        :param to_date: (unix) defines initial stop date of getting from binance.
        :param interval: interval of taking of currency values from binance in format 1M, 1d, 1m
         """
        get_tasks = [self.load_pair_history(pair='ETHUSDT',
                                            from_date=from_date,
                                            to_date=to_date,
                                            interval=interval),
                     self.load_pair_history(pair='BTCUSDT',
                                            from_date=from_date,
                                            to_date=to_date,
                                            interval=interval)
                     ]
        pair_history_responses = await asyncio.gather(*get_tasks)
        self.eth_btc_history_frame = await self.make_pair_history_data_frame(pair_history_responses)
        return self.eth_btc_history_frame

    async def get_recent_pair_data(self):
        pass


class DataManager:
    """
    Perform management of updating ETHUSDT, BTCUSDT pairs dataframe.
    Allow to define a period of time in which dataframe will contain unchanged and
    size of the dataframe.
    Necessary parameters to create an object:
    :param from_date: (unix) defines initial start date of getting from binance.
    :param to_date (unix) defines initial stop date of getting from binance.
    :param update_period (seconds): set how often dataframe will update.
    :param sample_time: how often will the data be sampled. For example: 1m, 1h, 1d, 1M.
    """
    def __init__(self, from_date, to_date, update_period, sample_time: str):
        self.eth_btc_history_frame = asyncio.Queue(1)
        self.update_period = update_period
        self.start_date = from_date
        self.stop_date = to_date
        self.sample_time = sample_time
        # Allow to stop update dataframe (turn it to False)
        self.update_allowed = True

    async def update_eth_btc_history_frame(self):
        self.start_date += self.update_period
        self.stop_date += self.update_period
        binance = BinanceGetDate()
        eth_btc_history_frame = await binance.load_pairs_history_frame(self.start_date,
                                                                       self.stop_date,
                                                                       interval=self.sample_time)
        await binance.session.close()
        await self.eth_btc_history_frame.put(eth_btc_history_frame)
        print('Hello updating in manager')

    def stop_updating(self):
        """ Call this method to stop update dataframe """
        self.update_allowed = False


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
