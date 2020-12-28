import cv2
import imutils
import logging
import requests
import time
import numpy as np

from api_code import post_image, send_sms

rtsp_url = "rtsp://david:cookies@192.168.0.142/live"

vs = cv2.VideoCapture() 
vs.open(rtsp_url)

starttime = time.time()
INTERVAL = 10.0 #seconds

time.sleep(10)

while True:
    print('tic')
    # Acquire image from Wyze Cam
    ret, frame = vs.read()
    if frame is None:
        continue
    frame = np.frombuffer(frame, dtype='uint8')

    print(frame.shape)
    result = post_image(frame)
    print(result)

     # Delay loop by INTERVAL
    time.sleep(INTERVAL - ((time.time() - starttime) % INTERVAL))
    break

# When everything done, release the capture 
vs.release()
vs.destroyAllWindows()