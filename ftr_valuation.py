import calendar

from ftr_auction_results_isone import get_auction_results
from ftr_utils import get_peak_offpeak_hours_in_year, get_peak_offpeak_hours_in_month, get_auction_year_month
from iso_lmp_data import load_monthly_lmp_data
import pandas as pd

# for day in iterate_days_in_month(2024, 9):
#     logger.info(f'Loading LMP for {day}')
#     df = load_isone_lmp_data(day.strftime('%Y%m%d'))
#     if not is_lmp_loaded(day):
#         logger.info(f"Saving LMP data to DB for {day.strftime('%Y%m%d')}")
#         save_isone_lmp_data(day, df)
#     else:
#         logger.info(f'Data exists for {day}')

# year, month = get_auction_year_month('LT1 2024')
# year1, month1 = get_auction_year_month('APR 2024 APR')

year = 2024
month = 3

monthly_auction_results = get_auction_results(year, month)


monthly_lmp = pd.read_csv(f"lmp_data/lmp_{year}_{month}.csv")


# monthly_lmp = load_monthly_lmp_data(year,month)
# monthly_lmp.to_csv(f"lmp_{year}_{month}.csv")



# for auction_file in os.listdir('auction_data'):
#     file = os.path.join('auction_data', auction_file)
#     load_auction_results(file)
#     logger.info(f'Processing auction file {file}')


print('Data Loaded')



