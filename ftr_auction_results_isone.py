import numpy as np
import pandas as pd

from ftr_utils import get_hour_price

#FTRs awarded in the off-peak auctions are valid for hours ending 2400 to 0700 on
#weekdays and for hours ending 0100 to 2400 on weekends and NERC Holidays.
# always sink minus source...and only need congestion...not LMP or losses


def get_auction_results(year: int, month: int):
    date_str = str(year) + "{:02d}".format(month)
    monthly_auction_file = f"auction_data/monthly_ftr_auction_results_{date_str}.csv"
    yearly_auction_file = f"auction_data/long_term_1_ftr_auction_results_{str(year)}.csv"

    monthly_auction_results = load_auction_results(monthly_auction_file)
    yearly_auction_results = load_auction_results(yearly_auction_file)

    monthly_auction_results = pd.concat([monthly_auction_results, yearly_auction_results])

    monthly_auction_results.drop(
        ['source_location_name', 'sink_location_name', 'source_location_type', 'sink_location_type', 'auction_file'],
        axis=1, inplace=True)

    return monthly_auction_results


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
    auction_df['source_location_id'] = pd.to_numeric(auction_df['source_location_id'], errors='coerce').fillna(
        0).astype(np.int64)
    auction_df['sink_location_id'] = pd.to_numeric(auction_df['sink_location_id'], errors='coerce').fillna(0).astype(
        np.int64)
    auction_file_name = input_file[input_file.find('/') + 1:].split('.')[0]
    auction_df['auction_file'] = auction_file_name

    auction_df['hour_price'] = auction_df.apply(
        lambda x: get_hour_price(x['price'], x['auction_name'], x['class_type']), axis=1)

    return auction_df
