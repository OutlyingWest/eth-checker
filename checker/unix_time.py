import datetime


def main():
    date_str = input('Enter time in format Y-m-d:')
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    get_unix_time_in_ms_utc(date_obj.year, date_obj.month, date_obj.day)


def get_unix_time_in_ms_utc(year, month, day):
    """ Returns time(ms) in unix format """
    date_obj = datetime.datetime(year, month, day)
    unix_timestamp = int(date_obj.replace(tzinfo=datetime.timezone.utc).timestamp()) * 1000
    return unix_timestamp


if __name__ == "__main__":
    main()
