import datetime


def main():
    pass


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


if __name__ == "__main__":
    main()
