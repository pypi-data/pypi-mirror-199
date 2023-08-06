nsebhavopy Python Package

This package provides a Python interface to download National Stock Exchange (NSE) bhavcopy data for Equities, Indices and Derivatives. The package provides functions to download daily bhavcopy data in CSV format, store the data in local storage, and update the data for any missing dates.

Basically it creates csv file for equities, indices and derivatives,
If the file already exist on assigned directory, then the code attempts to figure out missing dates and update the same file.
all you have to do is update the start and end date.

and all this can be done by simply providing following arguements:

pip install bhavcopy

import bhavcopy

# Place data need to be stored.

data_storage = "D:\\bhav_data"

# Define working directory, where files would be saved

os.chdir(data_storage)

# Define start and end dates, and convert them into date format

start_date = datetime.date(2023, 3, 1)

end_date = datetime.date(2023, 3, 21)

# Define wait time in seconds to avoid getting blocked

wait_time = [1, 2]

# Instantiate bhavcopy class for equities, indices, and derivatives

nse = bhavcopy("indices", start_date, end_date, data_storage, wait_time)

nse.get_data()

nse = bhavcopy("equities", start_date, end_date, data_storage, wait_time)

nse.get_data()

nse = bhavcopy("derivatives", start_date, end_date, data_storage, wait_time)

nse.get_data()

