import aiohttp
import asyncio


class BinanceGetDate:
    def __init__(self, ):
        self.session = aiohttp.ClientSession()

    async def get_pair_history(self, pair: str, from_date: int, to_date: int):
        async with self.session.get(
                f'https://api.binance.com/api/v3/klines?symbol={pair}&interval=1d&startTime={from_date}&endTime={to_date}'
        ) as response:
            print(await response.read())
