import cv2
import numpy as np
from statistics import mean, mode


def most_frequent(List): 
	return max(set(List), key = List.count) 

def calibratehsv(frame_init):
    cv2.imshow("Frame", frame_init)
    key = cv2.waitKey(1) & 0xFF
    colorRGB = []
    state = False
    if key == ord("s"):
        r = cv2.selectROI("Frame", frame_init, fromCenter=False,showCrosshair=True)
        frameCrop = frame_init[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        width = int(r[3])
        height = int(r[2])
        for x in range (0,height,1):
            for y in range(0,width,1):
                color = frameCrop[y,x]
                colorRGB.append((color[0], color[1], color[2]))
        mode_colorRGB = most_frequent(colorRGB)
        pixel = np.uint8([[mode_colorRGB]])
        hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
        #print(mode_colorRGB)
        #print(pixel)
        hsv = (int(hsv[0][0][0]), int(hsv[0][0][1]), int(hsv[0][0][2]))
        state = True
    if state == True:
        #hsv2 = cv2.cvtColor(frame_init, cv2.COLOR_BGR2HSV)
        lower = (hsv[0], 120, 120)
        upper = (hsv[0]+10, 255, 255)
        rangevalues = [lower, upper]
        #image_mask = cv2.inRange(hsv2,lower,upper)
        #cv2.imshow("Mask",image_mask)
        return rangevalues