# Simpson classifier Service

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth

import numpy as np
import cv2
import time
from model import SimpsonClassifier

import werkzeug
import os

# Instantiate the app
app = Flask(__name__)

CORS(app)
api = Api(app)

auth = HTTPBasicAuth()

USER_DATA = {
    "david": "cookiesandcream"
}


UPLOAD_FOLDER = 'static/img'
parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


def read_image(file):
    '''Convert file byte object to cv2 image numpy array'''
    filestr = file.read()
    # convert string data to numpy array
    nparr = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


class PhotoUpload(Resource):
    @auth.login_required
    def post(self):
        data = parser.parse_args()
        photo = data.get('file', None)
        print(photo)
        if photo:
            # filename = 'your_image.png'
            # save image to disk
            # photo.save(os.path.join(UPLOAD_FOLDER,filename))

            # read image file
            img = read_image(photo)
            img_size = 64
            img = cv2.resize(img, (img_size, img_size)
                             ).astype('float32') / 255.
            img = np.expand_dims(img, axis=0)

            # Instantiate model
            model = SimpsonClassifier(
                weights_path='./data/weights.best.hdf5', pic_size=img_size)

            # Run model
            result = model.run(img)
            # 	return {"y_pred": result['y_pred'], "y_prob": result['y_prob']}
            return {
                'y_pred': result["y_pred"],
                'y_prob': result["y_prob"]
            }
        return {
            'message': 'Something when wrong',
            'status': 'error'
        }


api.add_resource(HelloWorld, '/')
api.add_resource(PhotoUpload, '/upload')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
