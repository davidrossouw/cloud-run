import subprocess
import requests
import json
import cv2
import time
import io
import numpy as np


DIALPAD_API_KEY = str(subprocess.check_output("echo $DIALPAD_API_KEY", shell=True), 'utf-8').strip()
DIALPAD_USER_ID = str(subprocess.check_output("echo $DIALPAD_USER_ID", shell=True), 'utf-8').strip()
MY_PHONE_NUMBER = str(subprocess.check_output("echo $MY_PHONE_NUMBER", shell=True), 'utf-8').strip() 
IMAGE_PATH = '/Users/david/Documents/my_projects/cloud-run/wyze/images/cat1.jpg'

def post_image(img) -> dict:
    '''
    Post image to object detection API. Return the model output json
    '''
    # Prepare headers for http request
    google_token = str(
        subprocess.check_output("echo $(gcloud config config-helper --format 'value(credential.id_token)')", shell=True), 
        'utf-8').strip() 
    url = 'https://object-detection-2xihskugxq-ue.a.run.app/predict'
    headers = {'Authorization': 'Bearer ' + google_token, 'content_type': 'image/jpeg'}
    
    # Encode
    #print('ORG IMG: ', type(img), img.dtype, img.shape, img)
    
    img = cv2.imread(cv2.imdecode(img, cv2.IMREAD_UNCHANGED))
    print('working img: ', type(img), img.dtype, img.shape, img)

    is_success, buffer = cv2.imencode(".jpg", img)
    files = {'image': buffer}


    # Post request
    response = requests.request("POST", url, headers=headers, files=files)
    
    return json.loads(response.text.encode('utf8'))[0]



def send_sms(text:str) -> dict:
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
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    return json.loads(response.text.encode('utf8'))[0]
