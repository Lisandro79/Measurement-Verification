import eemeter
from flask import Flask
from flask import request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/data/'
ALLOWED_EXTENSIONS = {'json'}

# Inputs
# csv: datetime (1/1/19 0:00), eload (kWh), Temp (F)
# Baseline start date - Baseline end date
# Reporting start date - reporting end date
# $/kWh

# ToDo
# Front End:
#   - plots baseline and Reporting period.
#   - If the user agrees -> transform data into json format, add all inputs and send data to backend
# Backend:
#   - Create endpoint to receive csv and return a csv
#   - gets csv data, preprocess it into dataframe format
#   - Fits TOWT to the baseline, predicts energy consumption for reporting if no measure was taken
#   - Returns:
#       - json with temperature - baseline + fit, reporting + fit
#       - Model uncertainty
#       - Savings (kWh + $)

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save(UPLOAD_FOLDER)
    return 'File uploaded'


def main():
    # meter_data, temperature_data, sample_metadata = (
    #     eemeter.load_sample("il-electricity-cdd-hdd-hourly")
    # )
    #
    print("high")
    # meter_data.head()


if __name__ == '__main__':
    main()
