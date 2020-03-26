import cv2
import numpy as np
import imutils
import argparse
import math
import time

def nothing(x):
    pass


cap = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480
frame_center = 240
cap.set(3, frame_width)
cap.set(4, frame_height)

t_end = time.time() + 10

while (True):
    ret, frame = cap.read()
    if ret == True:
        frame_new = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame_new, cv2.COLOR_BGR2HSV)
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
        cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            area = cv2.contourArea(c)
            print(area)
            if(area > 20):
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 5, 2)

        cv2.imshow("Frame", frame)
        cv2.imshow("mask", eroded)

        result = cv2.bitwise_and(frame, frame, mask=eroded)
        cv2.imshow("Result", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
