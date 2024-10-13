import datetime
from datetime import timedelta

import numpy as np
import pandas as pd
from sqlalchemy import text

from ftr_logger import logger
from ftr_utils import get_db_connection, is_lmp_loaded, iterate_days_in_month, peak_offpeak


def load_monthly_lmp_data(year: int, month: int) -> pd.DataFrame:

    df = pd.DataFrame()

    for day in iterate_days_in_month(year, month):
        logger.info(f'Loading LMP for {day}')
        df = pd.concat([df,load_isone_lmp_data(day.strftime('%Y%m%d'))])

    return df


def load_isone_lmp_data(date: str) -> pd.DataFrame:

    logger.info(f'Loading isone lmp data for {date}')
    lmp_df = pd.read_csv(
        f'https://www.iso-ne.com/static-transform/csv/histRpts/da-lmp/WW_DALMP_ISO_{date}.csv',
        skiprows=[0, 1, 2, 3, 5]
    )
    logger.info('http GET finished')

    lmp_df = lmp_df[lmp_df.H == 'D']
    lmp_df.drop('H', axis=1, inplace=True)

    lmp_df.rename(columns={"Hour Ending": "he", "Location ID": "location_id", "Location Type": "location_type",
                           "Location Name": "location_name", "Locational Marginal Price": "lmp",
                           "Energy Component": "energy", "Congestion Component": "congestion",
                           "Marginal Loss Component": "loss", "Date": "date"}, inplace=True)

    lmp_df['he'] = pd.to_numeric(lmp_df['he'], errors='coerce').fillna(0).astype(np.int64)
    lmp_df['location_id'] = pd.to_numeric(lmp_df['location_id'], errors='coerce').fillna(0).astype(np.int64)
    lmp_df['datetime'] = pd.to_datetime(lmp_df['date'], format='%m/%d/%Y', errors='coerce')
    lmp_df['datetime'] = lmp_df.apply(lambda x: x['datetime'] + timedelta(hours=x['he']), axis=1)
    lmp_df['class_type'] = lmp_df.apply(lambda x: peak_offpeak(x['datetime']), axis=1)  #

    logger.info(f'Finished oading isone lmp data for {date}')

    return lmp_df


def save_isone_lmp_data(day: datetime.date, lmp_df: pd.DataFrame, replace: bool = False) -> None:

    with get_db_connection() as connection:

        if replace:
            logger.info('Replacing existing isone lmp data')
            result = connection.execute(text("delete from isone_lmp where date = '{}' limit 1"
                                             .format(day.strftime('%m/%d/%Y'))))
        if not is_lmp_loaded(day):
            logger.info(f'Saving isone lmp data for {day.strftime("%m/%d/%Y")}')
            lmp_df.to_sql("isone_lmp", connection, if_exists='append', index=False)
            logger.info('Data successfully saved')
            logger.info(f'Loaded isone lmp data for {day.strftime("%m/%d/%Y")}')


# https://www.iso-ne.com/transform/csv/ftrauctionresults?type=long_term_1&year=2024
