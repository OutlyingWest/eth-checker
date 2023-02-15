import aiohttp
import asyncio
import json
import pandas as pd
from pprint import pprint
from unix_time import convert_to_unix_time_by_input


async def main():
    # print('Start date of period')
    # from_date = convert_to_unix_time_by_input()
    # print('Stop date of period')
    # to_date = convert_to_unix_time_by_input()
    from_date = 1640995200000
    to_date = 1643673599999
    binance = BinanceGetDate()
    pair_history = await binance.get_pair_history(pair='ETHBTC', from_date=from_date, to_date=to_date)
    pprint(pair_history)
    await binance.session.close()


class BinanceGetDate:
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

    async def load_pairs_history_frame(self, from_date, to_date):
        """ Load data about ETHUSDT, BTCUSDT and close price time for a period """
        get_tasks = [self.load_pair_history(pair='ETHUSDT',
                                            from_date=from_date,
                                            to_date=to_date),
                     self.load_pair_history(pair='BTCUSDT',
                                            from_date=from_date,
                                            to_date=to_date)
                     ]
        pair_history_responses = await asyncio.gather(*get_tasks)
        await self.session.close()
        self.eth_btc_history_frame = await self.make_pair_history_data_frame(pair_history_responses)
        return self.eth_btc_history_frame

    async def get_recent_pair_data(self):
        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
