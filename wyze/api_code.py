import subprocess
import requests
import json

DIALPAD_API_KEY = str(subprocess.check_output("echo $DIALPAD_API_KEY", shell=True), 'utf-8').strip()
DIALPAD_USER_ID = str(subprocess.check_output("echo $DIALPAD_USER_ID", shell=True), 'utf-8').strip()
MY_PHONE_NUMBER = str(subprocess.check_output("echo $MY_PHONE_NUMBER", shell=True), 'utf-8').strip() 
IMAGE_PATH = '/Users/david/Documents/my_projects/cloud-run/wyze/images/cat1.jpg'

# Post image to object detection API
google_token = str(
    subprocess.check_output("echo $(gcloud config config-helper --format 'value(credential.id_token)')", shell=True), 
    'utf-8').strip() 
url = 'https://object-detection-2xihskugxq-ue.a.run.app/predict'
files = {'image': open(IMAGE_PATH,'rb')}
headers = { 'Authorization': 'Bearer ' + google_token}
response = requests.request("POST", url, headers=headers, files=files)
result = json.loads(response.text.encode('utf8'))[0]
print(result)

# Send SMS to phone
url = "https://dialpad.com/api/v2/sms"
querystring = {"apikey": DIALPAD_API_KEY}
payload = {
    "to_numbers": [MY_PHONE_NUMBER],
    "text": f"A {result['object']} was found!",
    "user_id": DIALPAD_USER_ID
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
print(response.text)