import calendar
import datetime

from sqlalchemy import create_engine, Connection, text


def iterate_days_in_month(year, month):
    """Iterate through each day in the specified month."""

    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, calendar._monthlen(year, month))

    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += datetime.timedelta(days=1)


def get_db_connection() -> Connection:
    conn_string = 'postgresql+psycopg://postgres:postgres@localhost:5432'
    db = create_engine(conn_string)
    return db.connect()


def is_lmp_loaded(day: datetime.date) -> bool:
    with get_db_connection() as connection:
        result = connection.execute(
            text("select * from isone_lmp where datetime = :day limit 1"), {"day": datetime.datetime(day.year, day.month, day.day, 1, 0, 0)})
        return result.rowcount == 1


def is_auction_file_loaded(auction_file: str) -> bool:
    with get_db_connection() as connection:
        result = connection.execute(text("select auction_file from isone_auction where auction_file = '{}' limit 1"
                                         .format(auction_file.split('.')[0])))
        return result.rowcount == 1


def peak_offpeak(date_time) -> str:
    if date_time.day_of_week > 4:
        return 'OFFPEAK'
    return 'ONPEAK' if 7 <= date_time.hour <= 23 else 'OFFPEAK'


def get_peak_offpeak_hours_in_month(year, month) -> (int, int):
    peak = 0
    off_peak = 0

    for day in iterate_days_in_month(year, month):
        if day.weekday() <= 4:
            peak += 16
            off_peak += 8
        else:
            off_peak += 24

    return peak, off_peak


def get_peak_offpeak_hours_in_year(year) -> (int, int, int):
    peak = 0
    off_peak = 0
    total_hours = 0

    for month in range(1, 13):
        for day in iterate_days_in_month(year, month):
            if day.weekday() <= 4:
                peak += 16
                off_peak += 8
            else:
                off_peak += 24
            total_hours += 24

    return peak, off_peak,


def get_auction_year_month(auction_name) -> (int, int):
    auction_year_split = auction_name.split(' ')
    if len(auction_year_split) == 2:
        return int(auction_year_split[1]), 0
    if len(auction_year_split) == 3:
        month_number = datetime.datetime.strptime(auction_year_split[2], '%b').month
        return int(auction_year_split[1]), month_number
    return 0, 0


def get_hour_price(price: float, auction_name: str, class_type: str) -> float:
    year, month = get_auction_year_month(auction_name)
    if month == 0:
        peak_hours, off_peak_hours = get_peak_offpeak_hours_in_year(year)
    else:
        peak_hours, off_peak_hours = get_peak_offpeak_hours_in_month(year, month)

    if class_type == 'ONPEAK':
        return price / peak_hours
    else:
        return price / off_peak_hours
