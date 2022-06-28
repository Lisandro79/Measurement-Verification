import pandas as pd
import json


dataset = pd.read_csv('data/WFM/dfhbt.csv')

# Parameters
start_baseline = dataset.loc[0, 'time']
end_baseline = "12/31/2019"
start_reporting = '01/01/2020'
end_reporting = '1/28/2020'
price_kWh = 0.3
user_name = 'Lolo'
project_name = 'Test'

time = dataset['time'].to_list()
eload = dataset['eload'].to_list()
temp = dataset['Temp'].to_list()

content = {
    'start_baseline': start_baseline,
    'end_baseline': end_baseline,
    'start_reporting': start_reporting,
    'end_reporting': end_reporting,
    'price_kWh': price_kWh,
    'user_name': user_name,
    'project_name': project_name,
    'time': time,
    'eload': eload,
    'temp': temp
}

with open('./data/test_data.json', 'w') as out_file:
    json.dump(content, out_file, indent=6)

