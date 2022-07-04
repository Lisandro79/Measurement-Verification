import eemeter
import json
import numpy as np
import pandas as pd
import pytz
import matplotlib.pyplot as plt


# First CALTRACK
# THEN https://github.com/LBNL-ETA/loadshape

with open('./data/template_data.json') as file:
    response = json.load(file)

# print('Commonly used time-zones:',
#       pytz.common_timezones, '\n')

eload = response['baseline_eload']
eload[-1] = np.nan
baseline_meter_data = pd.DataFrame(
    {"value": eload},
    index=pd.DatetimeIndex(data=response['baseline_datetime'], tz='UTC', freq='H', name="start")
)

temp = response['baseline_temp']
temperature_data = pd.Series(
    temp,
    index=pd.date_range(response['baseline_datetime'][0], response['baseline_datetime'][-1], freq='H', tz='UTC')
)

# create a design matrix for occupancy and segmentation
preliminary_design_matrix = (
    eemeter.create_caltrack_hourly_preliminary_design_matrix(
        baseline_meter_data, temperature_data,
    )
)

# build 12 monthly models - each step from now on operates on each segment
segmentation = eemeter.segment_time_series(
    preliminary_design_matrix.index,
    'three_month_weighted'
)

# assign an occupancy status to each hour of the week (0-167)
occupancy_lookup = eemeter.estimate_hour_of_week_occupancy(
    preliminary_design_matrix,
    segmentation=segmentation,
)

# assign temperatures to bins
occupied_temperature_bins, unoccupied_temperature_bins = eemeter.fit_temperature_bins(
    preliminary_design_matrix,
    segmentation=segmentation,
    occupancy_lookup=occupancy_lookup,
)

# build a design matrix for each monthly segment
segmented_design_matrices = (
    eemeter.create_caltrack_hourly_segmented_design_matrices(
        preliminary_design_matrix,
        segmentation,
        occupancy_lookup,
        occupied_temperature_bins,
        unoccupied_temperature_bins,
    )
)

# build a CalTRACK hourly model
baseline_model = eemeter.fit_caltrack_hourly_model(
    segmented_design_matrices,
    occupancy_lookup,
    occupied_temperature_bins,
    unoccupied_temperature_bins,
)

eload = response['reporting_eload']
eload[-1] = np.nan
reporting_meter_data = pd.DataFrame(
    {"value": eload},
    index=pd.DatetimeIndex(data=response['reporting_datetime'], tz='UTC', freq='H', name="start")
)

temp = response['reporting_temp']
temperature_reporting = pd.Series(
    temp,
    index=pd.date_range(response['reporting_datetime'][0], response['reporting_datetime'][-1], freq='H', tz='UTC')
)
# compute metered savings for the year of the reporting period we've selected
metered_savings_dataframe, error_bands = eemeter.metered_savings(
    baseline_model, reporting_meter_data,
    temperature_reporting, with_disaggregated=True
)

# total metered savings
total_metered_savings = metered_savings_dataframe.metered_savings.sum()


metered_savings_dataframe.plot(y=['reporting_observed', 'counterfactual_usage'])

