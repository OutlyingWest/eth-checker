import asyncio
import datetime
from asyncio.exceptions import InvalidStateError


def main():
    print(time_to_seconds(days=1))


def convert_to_unix_time_ms(year, month, day):
    """ Returns time(ms) in unix format UTC """
    date_obj = datetime.datetime(year, month, day)
    unix_timestamp = int(date_obj.replace(tzinfo=datetime.timezone.utc).timestamp()) * 1000
    return unix_timestamp


def convert_date_to_unix_time_by_input():
    """
    Allow to enter time in format Y-m-d.
    Returns time(ms) in unix format UTC.
    """
    date_str = input('Enter time in format Y-m-d:')
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    unix_time = convert_to_unix_time_ms(date_obj.year, date_obj.month, date_obj.day)
    return unix_time


def convert_date_to_unix_time_by_string(date_str: str):
    """
    Allow to enter time in format Y-m-d.
    Returns time(ms) in unix format UTC.
    """
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    unix_time = convert_to_unix_time_ms(date_obj.year, date_obj.month, date_obj.day)
    return unix_time


def time_to_seconds(**kwargs):
    """
    Convert time in hours to seconds.
    Available kwargs: minutes, hours, days
    """
    if len(kwargs) > 1:
        raise ValueError('Too much arguments.')
    if kwargs.get('minutes'):
        return int(kwargs.get('minutes')) * 60
    elif kwargs.get('hours'):
        return int(kwargs.get('hours')) * 3600
    elif kwargs.get('days'):
        return int(kwargs.get('days')) * 3600 * 24


class ResponseTimer:
    def __init__(self):
        # self.task = asyncio.create_task(self._run(timeout))
        self.timeout_passed_queue = asyncio.Queue(1)
        self.restarted = True

    async def run(self, timeout):
        while True:
            if self.restarted:
                start_time = asyncio.get_running_loop().time()
                elapsed_time = 0
                while elapsed_time < timeout:
                    elapsed_time = asyncio.get_running_loop().time() - start_time
                    # Wait for 1 second before checking again
                    await asyncio.sleep(1)
                self.restarted = False
                await self.timeout_passed_queue.put(True)
            else:
                await asyncio.sleep(1)

    def check_timer(self):
        if self.timeout_passed_queue.full():
            return True
        return False

    async def restart(self):
        self.restarted = True
        await self.timeout_passed_queue.get()


if __name__ == "__main__":
    main()
