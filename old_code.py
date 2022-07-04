from werkzeug.utils import secure_filename
import json


filename = secure_filename('my_file.json')
with open(UPLOAD_FOLDER + filename, 'w') as file:
    json.dump(response, file)

