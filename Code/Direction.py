import cv2
import numpy as np
import imutils
import argparse
import math
import time
from Find_Red import get_red

cap = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480
frame_center = 240
cap.set(3, frame_width)
cap.set(4, frame_height)

while (True):
    ret, frame = cap.read()
    if ret == True:
        cord = get_red(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
