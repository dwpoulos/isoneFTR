import datetime

from sqlalchemy import create_engine, Connection, text


def iterate_days_in_month(year, month):
    """Iterates through each day in the specified month."""

    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += datetime.timedelta(days=1)


def get_db_connection() -> Connection:
    conn_string = 'postgresql+psycopg://postgres:postgres@localhost:5432'
    db = create_engine(conn_string)
    return db.connect()


def is_lmp_loaded(date: datetime.date) -> bool:
    with get_db_connection() as connection:
        result = connection.execute(text("select date from isone_lmp where date = '{}' limit 1".format(date.strftime('%m/%d/%Y'))))
        return result.rowcount ==1

