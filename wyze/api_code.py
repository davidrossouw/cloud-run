import base64
import time
import subprocess
import requests
import json
import cv2
import time
import io
import numpy as np


DIALPAD_API_KEY = str(subprocess.check_output(
    "echo $DIALPAD_API_KEY", shell=True), 'utf-8').strip()
DIALPAD_USER_ID = str(subprocess.check_output(
    "echo $DIALPAD_USER_ID", shell=True), 'utf-8').strip()
MY_PHONE_NUMBER = str(subprocess.check_output(
    "echo $MY_PHONE_NUMBER", shell=True), 'utf-8').strip()
API_URL = 'https://object-detection-2xihskugxq-ue.a.run.app/predict'
#API_URL = 'http://0.0.0.0:8080/predict'


def post_image(img) -> dict:
    '''
    Post image to object detection API. Return the model output json
    '''

    # Encode image for API POST
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
    encode_state, img = cv2.imencode('.jpg', img, encode_params)

    # Prepare headers for http request
    url = API_URL
    headers = {'Authorization': 'Basic ZGF2aWQ6Y29va2llc2FuZGNyZWFt',
               'content_type': 'image/jpeg'}
    files = {'image': img}

    # Post request
    response = requests.request("POST", url, headers=headers, files=files)

    return json.loads(response.text.encode('utf8'))


def send_sms(text: str) -> dict:
    '''Send SMS to phone'''
    url = "https://dialpad.com/api/v2/sms"
    querystring = {"apikey": DIALPAD_API_KEY}
    payload = {
        "to_numbers": [MY_PHONE_NUMBER],
        "text": text,
        "user_id": DIALPAD_USER_ID
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring)
    return json.loads(response.text.encode('utf8'))
