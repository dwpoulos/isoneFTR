from ftr_utils import iterate_days_in_month, is_lmp_loaded
from iso_lmp_data import load_isone_lmp_data

load_isone_lmp_data('20240901')

for day in iterate_days_in_month(2024, 9):
    if not is_lmp_loaded(day):
        load_isone_lmp_data(day.strftime('%Y%m%d'))

print('Data Loaded')



