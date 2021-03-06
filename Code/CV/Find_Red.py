import cv2
import numpy as np
import imutils
import argparse
import math
import time

def get_red(frame):
    frame = cv2.flip(frame, 0)
    frame_new = cv2.GaussianBlur(frame, (5, 5), 0)
    #------------------Brightness Normalization----------
    YUV = cv2.cvtColor(frame_new, cv2.COLOR_BGR2YUV)
    Y, U, V = cv2.split(YUV)
    frame_new2 = cv2.equalizeHist(Y)
    frame_new4 = cv2.merge((frame_new2, U, V))
    frame_new3 = cv2.cvtColor(frame_new4, cv2.COLOR_YUV2BGR)
    #--------------------
    hsv = cv2.cvtColor(frame_new3, cv2.COLOR_BGR2HSV)
    colorLower = (0, 120, 170)
    colorUpper = (10, 255, 255)
    colorLower2 = (170, 120, 150)
    colorUpper2 = (180, 255, 255)

    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask2 = cv2.inRange(hsv, colorLower2, colorUpper2)
    mask_final = mask + mask2
    kernel = np.ones((3,3),np.uint8)
    eroded = cv2.erode(mask_final, kernel, iterations=0)
    #dilated = cv2.dilate(mask_final, kernel, iterations=3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    values = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), 0]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(c)
        #print(area)
        if(area > 20):
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            x2, y2, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame_new3, (x2, y2), (x2+w, y2+h), (0, 255, 0), 2)
            cv2.circle(frame_new3, (int(x), int(y)), int(radius), (255, 255, 255), 5, 2)
            values = [(x2, y2), (x2+w,y2), (x2,y2+h), (x2+w,y2+h), (int(x),int(y)), int(radius)]
            #print(values)
        else:
            values = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), 0]
    cv2.putText(frame_new3,str(values),(10,30), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Result", frame_new3)
    return values