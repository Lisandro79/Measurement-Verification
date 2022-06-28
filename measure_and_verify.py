import eemeter
import pandas as pd
import holidays
from datetime import datetime
import pytz
import numpy as np


def sanity_check():
    # column names, value types, dates format
    pass


def preprocess_data():
    # Decode from json
    # datetime, meter_data, temperature_data, metadata


    meter_data = dataset.loc[:, ['time', 'eload']].set_index('time')
    meter_data.index.name = 'start'
    meter_data.columns = ['value']

    # temperature_data = dataset.loc[:, ['time', 'Temp']]

    # get baseline data / reporting data
    # baseline_end_date = datetime(2019, 12, 31, tzinfo=pytz.UTC)
    baseline_meter_data, warnings = eemeter.get_baseline_data(
        meter_data, end=end_baseline, max_days=365
    )

    print('here')


def run_model():
    pass


def main():
    preprocess_data()


if __name__ == '__main__':
    main()
