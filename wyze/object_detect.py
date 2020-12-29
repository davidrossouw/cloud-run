import cv2
import requests

from api_code import post_image, send_sms

RTSP_URL = "rtsp://david:cookies@192.168.0.142/live"

cap = cv2.VideoCapture()
cap.open(RTSP_URL)

retval, frame = cap.read()
results = post_image(frame)
for result in results:
    print(f"A {result['object']} was found!")
    res = send_sms(f"A {result['object']} was found!")
    print(res)

# When everything done, release the capture
cap.release()