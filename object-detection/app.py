import cv2
import datetime
import gspread
import json
import logging
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

import tensorflow as tf
import tensorflow_hub as hub
import time

from auth import gcloud_auth
from flask import Flask, request, jsonify
from pytz import timezone

import pdb

app = Flask(__name__)
tf.get_logger().setLevel(logging.ERROR)
logger = logging.getLogger('app')

# Ayth gspread
gc = gspread.service_account(filename='/Users/davidrossouw/Downloads/my-cloud-run-284115-09ac85e52b57.json')
# Move the downloaded file to ~/.config/gspread/credentials.json
worksheet = gc.open_by_key('1snnHZayZn6PcqsVMyh_v68H51rqPmXDbZ4NQjPNRdEA').sheet1


@app.before_request
def authenticate_request():
    """Authenticates every request."""
    gcloud_auth(request.headers.get('Authorization'))

def convert_bounding_boxes(im_height, im_width, boxes):
  """
  """
  image_boxes = []
  for box in boxes:
      ymin, xmin, ymax, xmax = box
      image_boxes.append([int(xmin * im_width), int(ymin * im_height), int(xmax * im_width), int(ymax * im_height)])
  
  return image_boxes


def append_row_to_sheet(data, worksheet):

    #insert on the next available row
    timestamp = datetime.datetime.now(timezone('America/Toronto')).strftime("%Y/%m/%d %H:%M:%S")
    n_rows = len(data['detection_classes'])
    for row in range(n_rows):
        worksheet.append_row([
            timestamp,
            data['detection_classes'][row],
            data['detection_scores'][row],
            data['detection_boxes'][row][0],
            data['detection_boxes'][row][1],
            data['detection_boxes'][row][2],
            data['detection_boxes'][row][3]
        ])

    #worksheet.update(f"D{next_row}:G{next_row+n_rows}", [[d] for d in data['detection_boxes']])


def upload_image_to_gcs():
    pass
    


@app.route('/', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'there')
    # Write a log entry
    logger.info('who: %s', who)

    return f'Hello {who}!\n'




@app.route('/predict', methods=['POST'])
def predict():
    logger.setLevel(40)
    start = time.time()
    DETECTION_THRESHOLD = 0.7

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
    detection_boxes = out['detection_boxes'][0][:NUM_RESULTS].tolist()
    
    # convert boxes to image pixel co_ords
    result['detection_boxes'] = convert_bounding_boxes(
        im_height=np_img.shape[1],
        im_width=np_img.shape[2],
        boxes=detection_boxes
    )


    detection_classes = out['detection_classes'][0][:NUM_RESULTS].tolist()
    result['detection_classes'] = [label_map[int(i)] for i in detection_classes]
    end = time.time()
    execution_time = round(end - start, 2)
    msg = f"Success! Total execution time: {execution_time} sec."
    logger.info(msg)

    # Write to sheet
    append_row_to_sheet(data=result, worksheet=worksheet)

    return jsonify(result)


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=int(
        os.environ.get('PORT', 8080)), debug=True, use_reloader=False)
