# Import libraries
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)
servo1.start(0)

def move_servo(angle):
    try:
        servo1.ChangeDutyCycle(2.4 + angle/20.9302)
        time.sleep(0.1)
        servo1.ChangeDutyCycle(0)
        servo1.ChangeDutyCycle(2.4 + angle/20.9302)
        servo1.ChangeDutyCycle(0)
    except:
        print("Failed to move servo")

def clean_servo():
    servo1.stop()
    GPIO.cleanup()