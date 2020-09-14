import cv2
import json
import logging
import numpy as np
import os
import tensorflow as tf
import tensorflow_hub as hub
import time

# from auth import gcloud_auth
from flask import Flask, request, jsonify


app = Flask(__name__)

tf.get_logger().setLevel(logging.ERROR)
logger = logging.getLogger('app')


# @app.before_request
# def authenticate_request():
#     """Authenticates every request."""
#     gcloud_auth(request.headers.get('Authorization'))


# Load model
MODEL_PATH = './model/efficientdet_d0_1/'
print('loading model...')
hub_model = hub.load(MODEL_PATH)
print('model loaded!')
logger.info("model %s loaded" % MODEL_PATH)

# Load labels
LABELS_PATH = './mscoco_label_map.json'
with open(LABELS_PATH, 'r') as f:
    label_map = json.load(f)

label_map = {int(k):v for k,v in label_map.items()}
DETECTION_THRESHOLD = 0.7

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

    # Read image
    image = request.files["image"].read()
    np_img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_COLOR)
    np_img = np.expand_dims(np_img, axis=0)

    # Run model
    out = hub_model(np_img)

    # Trim results
    out = {key:value.numpy() for key,value in out.items()}
    NUM_RESULTS = (out['detection_scores'] >= DETECTION_THRESHOLD).sum()
    result = {}
    result['detection_scores'] = out['detection_scores'][0][:NUM_RESULTS].tolist()
    result['detection_boxes'] = out['detection_boxes'][0][:NUM_RESULTS].tolist()
    detection_classes = out['detection_classes'][0][:NUM_RESULTS].tolist()
    result['detection_classes'] = [label_map[int(i)] for i in detection_classes]
    end = time.time()
    execution_time = round(end - start, 2)
    msg = f"Success! Total execution time: {execution_time} sec."
    logger.info(msg)
    return jsonify(result)


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=int(
        os.environ.get('PORT', 8080)), debug=False)
