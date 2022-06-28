import eemeter
import pandas as pd
import holidays
from datetime import datetime
import pytz
import numpy as np


def sanity_check(response):
    # column names
    # value types (str | float)
    # dates format ('M-D-Y H:M'), two year vs 4 year digits
    # All variables / arrays must contain data (cannot be empty)
    # Reporting time, eload and temp arrays must have the same length
    # Baseline time, eload and temp arrays must have the same length
    pass


def run_model(response):
    sanity_check(response)

    # Occupancy

    # run models
    # meter_data = dataset.loc[:, ['time', 'eload']].set_index('time')
    # meter_data.index.name = 'start'
    # meter_data.columns = ['value']

    # temperature_data = dataset.loc[:, ['time', 'Temp']]

    # get baseline data / reporting data
    # baseline_end_date = datetime(2019, 12, 31, tzinfo=pytz.UTC)
    # baseline_meter_data, warnings = eemeter.get_baseline_data(
    #     meter_data, end=end_baseline, max_days=365
    # )

