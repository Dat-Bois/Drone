import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(26)
    if input_state == False:
        print('Button Pressed')
		os.system("sudo poweroff")
        time.sleep(0.2)