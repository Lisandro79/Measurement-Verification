import numpy as np
import pandas as pd
import json
from datetime import datetime


def filter_indexes_by_date(data, start, end):
    return (data >= datetime.strptime(start, format_str)) & \
           (data < datetime.strptime(end, format_str))


dataset = pd.read_csv('data/WFM/dfhbt.csv')

# Parameters
start_baseline = '1/1/19 0:00'
end_baseline = '12/31/19 0:00'
start_reporting = '01/01/20 0:00'
end_reporting = '1/28/20 0:00'
price_kWh = 0.3
user_name = 'Lolo'
project_name = 'Test'

time = dataset['time'].to_list()
eload = dataset['eload'].to_list()
temp = dataset['Temp'].to_list()

format_str = '%m/%d/%y %H:%M'
tt = [datetime.strptime(sample, format_str) for sample in time]
arr = np.array(tt)

idxs = filter_indexes_by_date(arr, start_baseline, end_baseline)
baseline_datetime = [tt for tt, idx in zip(time, idxs) if idx]
baseline_eload = [el for el, idx in zip(eload, idxs) if idx]
baseline_temp = [tmp for tmp, idx in zip(temp, idxs) if idx]

idxs = filter_indexes_by_date(arr, start_reporting, end_reporting)
reporting_datetime = [tt for tt, idx in zip(time, idxs) if idx]
reporting_eload = [el for el, idx in zip(eload, idxs) if idx]
reporting_temp = [tmp for tmp, idx in zip(temp, idxs) if idx]

content = {
    'project_name': project_name,
    'user_name': user_name,
    'start_baseline': start_baseline,
    'end_baseline': end_baseline,
    'start_reporting': start_reporting,
    'end_reporting': end_reporting,
    'price_kWh': price_kWh,
    'baseline_datetime': baseline_datetime,
    'baseline_eload': baseline_eload,
    'baseline_temp': baseline_temp,
    'reporting_datetime': reporting_datetime,
    'reporting_eload': reporting_eload,
    'reporting_temp': reporting_temp
}

with open('./data/template_data.json', 'w') as out_file:
    json.dump(content, out_file, indent=6)

