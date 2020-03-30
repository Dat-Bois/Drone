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

k_distance = 7.5
k_width = 0.75
k_pixWidth = 72
focal_length = (k_pixWidth * k_distance) / k_width
distance = 0
def distance_to_camera(width, focal_length, per_width):
    return int((width*focal_length) / per_width)

def centered(x, y, distance):
    max_right = 400
    max_left = 200
    max_up = 160
    max_down = 260
    max_close = 6
    max_far = 8
    if x >= max_left and x <= max_right and y >= max_up and y <= max_down and distance >= max_close and distance <= max_far:
            print("Centered at: ", center)
    else:
        if x >= max_left and x <= max_right:
            print("x-centered")
        elif x >= max_right:
            print("Move left")
        else:
            print("Move right")
        if y >= max_up and y <= max_down:
            print("y-centered")
        elif y >= max_down:
            print("Move up")
        else:
            print("Move down")
        if distance >= max_close and distance <= max_far:
            print("distance-centered")
        elif distance >= max_far:
            print("Move closer")
        else:
            print("Move farther")
while (True):
    ret, frame = cap.read()
    if ret == True:
        cord = get_red(frame)
        #-----Distance----
        width = cord[1][0] - cord[0][0]
        if width != 0:
            distance = distance_to_camera(k_width, focal_length, width)
            print(distance)
        #-----------------
        #----Center------
        center = cord[4]
        x = center[0]
        y = center[1]
        centered(x, y, distance)
        #-----------------
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
