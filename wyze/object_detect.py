import cv2
import logging
import requests
import time

from api_code import post_image, send_sms

RTSP_URL = "rtsp://david:cookies@192.168.0.142/live"
INTERVAL = 10.0  # seconds

cap = cv2.VideoCapture()  # 0?
cap.open(RTSP_URL)

starttime = time.time()

while True:

    start = time.time()
    while not (time.time() - start > INTERVAL):
        # delay here
        pass

    # Execute this plock after interval
    retval, frame = cap.read()
    results = post_image(frame)
    for result in results:
        print(f"A {result['object']} was found!")
        res = send_sms(f"A {result['object']} was found!")
        print(res)

# When everything done, release the capture
cap.release()
cap.destroyAllWindows()
