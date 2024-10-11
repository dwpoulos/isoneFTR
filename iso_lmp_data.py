from datetime import timedelta

import numpy as np
import pandas as pd

from ftr_utils import get_db_connection


def load_isone_lmp_data(date: str):
    lmp_df = pd.read_csv(
        f'https://www.iso-ne.com/static-transform/csv/histRpts/da-lmp/WW_DALMP_ISO_{date}.csv',
        skiprows=[0, 1, 2, 3, 5]
    )

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

    conn = get_db_connection()

    lmp_df.to_sql("isone_lmp", conn, if_exists='append', index=False)

# https://www.iso-ne.com/transform/csv/ftrauctionresults?type=long_term_1&year=2024
