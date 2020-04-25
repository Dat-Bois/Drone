import time
from logger import log, flush
import Movement

#--Initizialize the pixhawk for autonomous control
Movement.initialize()
Movement.initialization_check()
#Set speed of movement in meters per second
Movement.groundSpeed(0.5)
#Arm motors and takeoff in GUIDED mode
Movement.arm_and_takeoff(2)
#delay to check postion hold
time.sleep(4)
#Rotate 30 degrees clockwise
Movement.changeYaw(30, 1)
#Rotate 30 degrees counter-clockwise
Movement.changeYaw(30, -1)
#Land in place
Movement.land()

#Flushes all data to log file
Movement.flush_log("Main_Log")
