import base64
import cv2
import datetime
import json
import logging
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

import random
import tensorflow as tf
import tensorflow_hub as hub
import time

from auth import gcloud_auth
from google.cloud import storage, bigquery
from flask import Flask, request, jsonify
from pytz import timezone

from tempfile import NamedTemporaryFile

import pdb

app = Flask(__name__)
tf.get_logger().setLevel(logging.ERROR)
logger = logging.getLogger('app')

# Create BQ client
bq_client = bigquery.Client(project='my-cloud-run-284115')

# Load labels
LABELS_PATH = './mscoco_label_map.json'
with open(LABELS_PATH, 'r') as f:
    label_map = json.load(f)

label_map = {int(k):v for k,v in label_map.items()}

# Load model
MODEL_PATH = './model/efficientdet_d0_1/'
hub_model = hub.load(MODEL_PATH)
logger.setLevel(20) 
logger.info("model %s loaded" % MODEL_PATH)


@app.before_request
def authenticate_request():
    """Authenticates every request."""
    logger.setLevel(20) 
    gcloud_auth(request.headers.get('Authorization'), logger)

def convert_bounding_box(im_height, im_width, box):
  """
  """
  ymin, xmin, ymax, xmax = box
  return [int(xmin * im_width), int(ymin * im_height), int(xmax * im_width), int(ymax * im_height)]

def upload_blob(img, obj, timestamp):
    """Uploads a file to the bucket."""
    logger.setLevel(20) 
    logger.info(f'image shape: {img.shape}')
    storage_client = storage.Client(project='my-cloud-run-284115')
    bucket = storage_client.get_bucket('my-cloud-run-284115.appspot.com')

    buffer = cv2.imencode(".jpg", img)[1].tostring()
    #jpg_as_text = base64.b64encode(buffer)

    # Uploading from a local file using open()
    blob = bucket.blob(f'{timestamp}_{obj}.jpg')
    blob.upload_from_string(buffer, content_type='image/jpg')
    url = blob.public_url
    logger.info(f"image uploaded")
    
    return url


def pusher(client, data: dict) -> None:
    '''
    Push model results to new BQ table
    Table schema:
    [
    {
        "description":"timestamp",
        "name":"timestamp",
        "type":"TIMESTAMP",
        "mode":"REQUIRED"
    },
    {
        "description": "object",
        "name": "object",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "description": "score",
        "name": "score",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "description": "url",
        "name": "url",
        "type": "STRING",
        "mode": "REQUIRED"
    }
    ]
    '''
    logger.setLevel(20) 
    table_id = "my-cloud-run-284115.object_detection.results1"
    logger.info("Uploading data to BQ...")
    errors = client.insert_rows_json(table_id, data) 
    if errors == []:
        logger.info("New rows have been added.")
    else:
        logger.info("Encountered errors while inserting rows: {}".format(errors))
    return



@app.route('/', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'there')
    # Write a log entry
    logger.info('who: %s', who)

    return f'Hello {who}!\n'


@app.route('/test_predict', methods=['POST'])
def test():
    """Return a dummy result conforming to that expected from the predict endpoint """
    timestamp = datetime.datetime.now(timezone('America/Toronto')).strftime("%Y-%m-%d_%H:%M:%S")
    rnd = random.choice([0, 1])
    if rnd:
        results = [
            {'timestamp': timestamp,
             'object': 'dog',
             'score': 0.75,
             'url': 'www.url1.com'},
            {'timestamp': timestamp,
             'object': 'cat',
             'score': 0.85,
             'url': 'www.url2.com'}
        ]
        return jsonify(results)
    else:
        results = []
        return jsonify(results)

    

@app.route('/predict', methods=['POST'])
def predict():
    logger.setLevel(20)
    start = time.time()
    timestamp = datetime.datetime.now(timezone('America/Toronto')).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    DETECTION_THRESHOLD = 0.7

    # Read image
    image = request.files["image"].read()

    np_img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Run model
    out = hub_model(np.expand_dims(np_img, axis=0))
    out = {key:value.numpy() for key,value in out.items()}

    # Parse results
    NUM_RESULTS = (out['detection_scores'] >= DETECTION_THRESHOLD).sum()
    if not NUM_RESULTS:
        logger.info("No results")
        return []

    results = [] # list of dicts
    for i, row in enumerate(range(NUM_RESULTS)):
        obj = label_map[int(out['detection_classes'][0][row])],
        obj = obj[0]+'_'+str(i)
        # crop image
        box = convert_bounding_box(np_img.shape[0], np_img.shape[1], out['detection_boxes'][0][row])
        # Upload detected object images to GCS bucket
        url = upload_blob(img=np_img[box[1]:box[3], box[0]:box[2]], obj=obj, timestamp=timestamp)
        logger.info(f'blob uploaded to: {url}')

        results.append({
            'timestamp': timestamp,
            'object': obj,
            'score': round(out['detection_scores'][0][row], 2).astype(float),
            'url': url
        })

    ###
    end = time.time()
    execution_time = round(end - start, 2)
    logger.info(f"Success! Total execution time: {execution_time} sec.")
    logger.info(f"Results: {results}")

    # Write to BQ
    pusher(client=bq_client, data=results)

    return jsonify(results)


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=int(
        os.environ.get('PORT', 8080)), debug=True, use_reloader=False)
