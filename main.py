from flask import Flask, request, jsonify
import measure_and_verify
from measure_and_verify import format_temp_data, format_meter_data

app = Flask(__name__)
UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = ['application/json']


@app.route('/home', methods=['POST'])
def receive_data(response=None):
    content_type = request.headers.get('Content-Type')
    if content_type == ALLOWED_EXTENSIONS[0]:
        response = request.get_json()
        return measure_and_verify.cal_track(response)
    return jsonify(['Content Type Not Supported'])


if __name__ == '__main__':
    app.run(debug=False)
