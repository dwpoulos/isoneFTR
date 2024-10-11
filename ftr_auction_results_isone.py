import pandas as pd
from sqlalchemy import create_engine
import numpy as np

#FTRs awarded in the off-peak auctions are valid for hours ending 2400 to 0700 on
#weekdays and for hours ending 0100 to 2400 on weekends and NERC Holidays.

# always sink minus source...and only need congestion...not LMP or losses
# don't matter if it's DA or RT or DART..it's walays sink MINUS source


def load_auction_results(input_file: str) -> pd.DataFrame:

    auction_df = pd.read_csv(
        input_file,
        skiprows=[0, 1, 2, 3, 5]
    )

    auction_df = auction_df[auction_df.H == 'D']
    auction_df.drop('H', axis=1, inplace=True)
    auction_df.rename(columns={
        "Auction Name": "auction_name",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Source Location ID": "source_location_id",
        "Source Location Name": "source_location_name",
        "Source Location Type": "source_location_type",
        "Sink Location ID": "sink_location_id",
        "Sink Location Name": "sink_location_name",
        "Sink Location Type": "sink_location_type",
        "Buy/Sell": "buy_sell",
        "ClassType": "class_type",
        "Award FTR MW": "mw",
        "Award FTR Price": "price"
    }, inplace=True)

    auction_df['customer_id'] = pd.to_numeric(auction_df['customer_id'], errors='coerce').fillna(0).astype(np.int64)
    auction_df['source_location_id'] = pd.to_numeric(auction_df['source_location_id'], errors='coerce').fillna(0).astype(np.int64)
    auction_df['sink_location_id'] = pd.to_numeric(auction_df['sink_location_id'], errors='coerce').fillna(0).astype(np.int64)

    return auction_df


df = load_auction_results('data/monthly_ftr_auction_results_202410.csv')
print(df.head())

conn_string = 'postgresql+psycopg://postgres:postgres@localhost:5432'
db = create_engine(conn_string)
conn = db.connect()

df.to_sql("isone_auction", conn, if_exists='append', index=False)

print()

