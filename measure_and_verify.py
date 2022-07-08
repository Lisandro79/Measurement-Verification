import eemeter
import pandas as pd
import numpy as np
import simplejson
from memory_profiler import profile


def format_meter_data(date_time, meter_data):
    meter_data[-1] = np.nan
    return pd.DataFrame({"value": meter_data},
                        index=pd.DatetimeIndex(data=date_time,
                                               tz='UTC', freq='H',
                                               name="start"))


def format_temp_data(date_time, temp_data):
    return pd.Series(
        temp_data,
        index=pd.date_range(date_time[0], date_time[-1], freq='H', tz='UTC')
    )


# @profile
def cal_track(response):
    '''
    Fit CALTrack
    Return Baseline, Baseline fit, reporting, reporting prediction, energy savings, monetary savings
    model error estimation
   '''

    baseline_meter_data = format_meter_data(response['baseline_datetime'], response['baseline_eload'])
    baseline_temp = format_temp_data(response['baseline_datetime'], response['baseline_temp'])
    reporting_meter_data = format_meter_data(response['reporting_datetime'], response['reporting_eload'])
    reporting_temp = format_temp_data(response['reporting_datetime'], response['reporting_temp'])

    # create a design matrix for occupancy and segmentation
    preliminary_design_matrix = (
        eemeter.create_caltrack_hourly_preliminary_design_matrix(
            baseline_meter_data, baseline_temp,
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

    # Compute metered savings for the year of the reporting period we've selected
    metered_savings_dataframe, error_bands = \
        eemeter.metered_savings(baseline_model,
                                reporting_meter_data,
                                reporting_temp,
                                with_disaggregated=True
    )

    # metered_savings_dataframe.plot(y=['reporting_observed', 'counterfactual_usage'])
    response['reporting_counterfactual_usage'] = metered_savings_dataframe['counterfactual_usage'].to_list()
    # total metered savings
    response['meter_savings'] = metered_savings_dataframe.metered_savings.sum()
    # with open('template_response.json', 'w') as out_file:
    #     json.dump(response, out_file, indent=6)

    return simplejson.dumps(response, ignore_nan=True)


def sanity_check(response):
    # Column names in the dataset
    # Value types (str | float)
    # Dates format ('M-D-Y H:M'), two year vs 4 year digits
    # Reporting time, eload and temp arrays must have the same length
    # Baseline time, eload and temp arrays must have the same length
    # All vectors must contain data (cannot be empty)
    # Create occupancy vector??
    pass






