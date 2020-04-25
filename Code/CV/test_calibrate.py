from calibrate import calibratehsv
import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480
frame_center = 240
cap.set(3, frame_width)
cap.set(4, frame_height)

while (True):
    ret, frame = cap.read()
    if ret == True:
        rangehsv = calibratehsv(frame)
        print(rangehsv)
