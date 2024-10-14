import sys
from datetime import datetime

from iso_lmp_data import load_isone_lmp_data, save_isone_lmp_data

try:
    args = sys.argv[1]
    day = datetime.strptime(args, '%Y%m%d')

except IndexError:
    print("Error: Please provide a valid Day in the format:  YYYYMMDD.  Example 20240301.")
    sys.exit(0)

except ValueError:
    print("Error: Please provide a valid Day in the format:  YYYYMMDD.  Example 20240301.")
    sys.exit(0)


lmp_data = load_isone_lmp_data(args)
save_isone_lmp_data(day.date(), lmp_data, replace=False)