import sys

import numpy as np
import pandas as pd

from ftr_auction_results_isone import get_auction_results
from ftr_logger import logger
from iso_lmp_data import load_monthly_lmp_data

year = 2024
month = 3

try:
    args = sys.argv[1]
    input = args.split('/')
    month = int(input[0])
    year = int(input[1])

except IndexError:
    print("Error: Please provide a valid Month in the format:  MM/YYYY.  Example 03/2024.")
    sys.exit(0)

except ValueError:
    print("Error: Please provide a valid Month in the format:  MM/YYYY.  Example 03/2024.")
    sys.exit(0)


monthly_auction_results = get_auction_results(year, month)
monthly_lmp = load_monthly_lmp_data(year, month)

monthly_auction_results['buy_sell_adj'] = np.where((monthly_auction_results['buy_sell'] == 'BUY'),1,-1)

logger.info('Merging source lmp data')
# monthly_lmp.reset_index().set_index(['location_id','class_type'], inplace=True)
monthly_auction_results = pd.merge(monthly_auction_results, monthly_lmp[
    ['location_id', 'location_name', 'congestion', 'class_type', 'datetime']], how='left',
                                   left_on=['source_location_id', 'class_type'],
                                   right_on=['location_id', 'class_type'])
monthly_auction_results.drop(['location_id'], axis=1, inplace=True)
monthly_auction_results.rename(columns={
    "congestion": "source_congestion",
    "location_name": "source_location_name",
}, inplace=True)

logger.info('Merging sink lmp data')
# monthly_lmp.reset_index().set_index(['location_id', 'class_type', 'datetime'], inplace=True)
monthly_auction_results = pd.merge(monthly_auction_results, monthly_lmp[
    ['location_id', 'location_name', 'congestion', 'class_type', 'datetime']], how='left',
                                   left_on=['sink_location_id', 'datetime'],
                                   right_on=['location_id', 'datetime'])
monthly_auction_results.rename(columns={
    "congestion": "sink_congestion",
    "location_name": "sink_location_name",
}, inplace=True)
monthly_auction_results.drop(['location_id'], axis=1, inplace=True)

logger.info('Computing Revenue')
monthly_auction_results['revenue'] = (
        monthly_auction_results['mw'] *
        (monthly_auction_results['sink_congestion'] - monthly_auction_results['source_congestion']) *
        monthly_auction_results['buy_sell_adj']
)

logger.info('Computing Cost')
monthly_auction_results['cost'] = (monthly_auction_results['mw'] *
                                   monthly_auction_results['hour_price'] *
                                   -1 * monthly_auction_results['buy_sell_adj'])

logger.info('Computing Profit')
monthly_auction_results['profit'] = monthly_auction_results['cost'] + monthly_auction_results['revenue']

# Can do hourly/daily breakdown here

logger.info("Grouping Results")
profit_loss = monthly_auction_results[['customer_name','revenue','cost','profit']]
totals = monthly_auction_results.groupby(['customer_name'])[['revenue', 'cost', 'profit']].sum()

print('FTR Report Complete')
totals.to_csv(f'ftr_profit_loss{str(year)}{str(month)}.csv')
print(totals.head())
