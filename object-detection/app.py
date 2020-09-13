import cv2
import json
import logging
import numpy as np
import os
import tensorflow as tf
import tensorflow_hub as hub
import time

from auth import gcloud_auth
from flask import Flask, request, jsonify


app = Flask(__name__)

logger = logging.getLogger('app')


@app.before_request
def authenticate_request():
    """Authenticates every request."""
    gcloud_auth(request.headers.get('Authorization'))


# LOAD MODEL
MODEL_PATH = './model/faster_rcnn_inception_resnet_v2_640x640_1/'
print('loading model...')
hub_model = hub.load(MODEL_PATH)
print('model loaded!')
logger.info("model %s loaded" % MODEL_PATH)


@app.route('/', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'there')
    # Write a log entry
    logger.info('who: %s', who)

    return f'Hello {who}!\n'


@app.route('/predict', methods=['POST'])
def predict():
    start = time.time()
    image = request.files["image"].read()
    print("image :" ,type(image))
    np_img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    # read image file
    np_img = np.expand_dims(np_img, axis=0)

    ### Run model
    # running inference
    out = hub_model(np_img)
    result = {key:value.numpy() for key,value in out.items()}
    # trim for now
    result = result['detection_classes']
    print(result)
    ###
    end = time.time()
    execution_time = round(end - start, 2)
    msg = f"Success! Total execution time: {execution_time} sec. \n\
        Result: {result}"
    logger.info(msg)
    return jsonify(message=msg)


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=int(
        os.environ.get('PORT', 8080)), debug=True)
