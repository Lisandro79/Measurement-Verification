import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = ['application/json']


@app.route('/home', methods=['POST'])
def receive_data():
    content_type = request.headers.get('Content-Type')
    if content_type == ALLOWED_EXTENSIONS[0]:
        response = request.get_json()
        filename = secure_filename('my_file.json')
        with open(UPLOAD_FOLDER + filename, 'w') as file:
            json.dump(response, file)
        return jsonify(response)
    return jsonify(['Content Type Not Supported'])


if __name__ == '__main__':
    app.run(debug=True)
