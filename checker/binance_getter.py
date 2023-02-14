import aiohttp
import asyncio
import json
from pprint import pprint
from unix_time import convert_to_unix_time_by_input


async def main():
    print('Start date of period')
    from_date = convert_to_unix_time_by_input()
    print('Stop date of period')
    to_date = convert_to_unix_time_by_input()
    binance = BinanceGetDate()
    pair_history = await binance.get_pair_history(pair='ETHBTC', from_date=from_date, to_date=to_date)
    pprint(pair_history)
    await binance.session.close()


class BinanceGetDate:
    def __init__(self, ):
        self.session = aiohttp.ClientSession()

    async def get_pair_history(self, pair: str, from_date: int, to_date: int, interval='1d'):
        """ Returns pair history in json object """
        async with self.session.get(
                f'https://api.binance.com/api/v3/klines?' +
                f'symbol={pair}&interval={interval}&startTime={from_date}&endTime={to_date}'
        ) as response:
            klines_byte_string = await response.read()
            json_klines = json.loads(klines_byte_string)
            return json_klines

    async def get_recent_pair_data(self):
        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((main()))
