from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
from logger import log, flush

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=921600)

print "Autopilot Firmware version: %s" % vehicle.version
log("Autopilot Firmware version: " + str(vehicle.version))
#print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
#print "Global Location: %s" % vehicle.location.global_frame
#print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
#print "Local Location: %s" % vehicle.location.local_frame    #NED
#print "Attitude: %s" % vehicle.attitude
#print "Velocity: %s" % vehicle.velocity
print "GPS: %s" % vehicle.gps_0
log("GPS: " + str(vehicle.gps_0))
#print "Groundspeed: %s" % vehicle.groundspeed
#print "Airspeed: %s" % vehicle.airspeed
#print "Gimbal status: %s" % vehicle.gimbal
print "Battery: %s" % vehicle.battery
log("Battery: " + str(vehicle.battery))
#print "EKF OK?: %s" % vehicle.ekf_ok
#print "Last Heartbeat: %s" % vehicle.last_heartbeat
#print "Rangefinder: %s" % vehicle.rangefinder
#print "Rangefinder distance: %s" % vehicle.rangefinder.distance
#print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
#print "Heading: %s" % vehicle.heading
print "Is Armable?: %s" % vehicle.is_armable
log("Is Armable?: " + str(vehicle.is_armable))
print "System status: %s" % vehicle.system_status.state
log("System status: " + str(vehicle.system_status.state))
print "Mode: %s" % vehicle.mode.name    # settable
log("Mode: " + str(vehicle.mode.name))
print "Armed: %s" % vehicle.armed    # settable
log("Armed: " + str(vehicle.armed))

def arm_and_takeoff(targetAltitude):
    print("Arming Motors...")
    log("Arming Motors...")
    vehicle.mode = "GUIDED"
    print "Mode: %s" % vehicle.mode.name    # settable
    log("Mode: " + str(vehicle.mode.name))
    vehicle.armed = True
    while not vehicle.armed:
        print ("Waiting for arm...")
        log("Waiting for arm...")
        time.sleep(1)
    print("ARMED!")
    log("ARMED!")
    print("Taking Off")
    log("Taking Off")
    vehicle.simple_takeoff(targetAltitude)
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
        if (vehicle.location.global_relative_frame.alt >= targetAltitude*0.95):
            print("Reached Target Altitude")
            log("Reached Target Altitude")
            break
        time.sleep(1)

def land():
    print("landing now!")
    vehicle.mode = "LAND"
    while True:
            print (" Altitude: ", vehicle.location.global_relative_frame.alt)
            log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
            if (vehicle.location.global_relative_frame.alt <= 0):
                print("Landed!")
                log("Landed!")
                break
            time.sleep(1)

def setAlt(targetAltitude):
    loc = vehicle.LocationGlobalRelative
    loc.alt = targetAltitude
    vehicle.simple_goto(loc)
    if (vehicle.LocationGlobalRelative.alt <= targetAltitude):
        while True:
            print (" Altitude: ", vehicle.location.global_relative_frame.alt)
            log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
            if (vehicle.location.global_relative_frame.alt >= targetAltitude*0.95):
                print("Reached Target Altitude")
                log("Reached Target Altitude")
                return
            time.sleep(1)
    if (vehicle.LocationGlobalRelative.alt >= targetAltitude):
        while True:
            print (" Altitude: ", vehicle.location.global_relative_frame.alt)
            log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
            if (vehicle.location.global_relative_frame.alt <= targetAltitude*1.05):
                print("Reached Target Altitude")
                log("Reached Target Altitude")
                return
            time.sleep(1)

def changeAlt(changeAltitude):
    currentAlt = vehicle.LocationGlobalRelative.alt
    targetAlt = currentAlt + changeAltitude
    setAlt(targetAlt)

vehicle.groundspeed = 2
arm_and_takeoff(0.5)
time.sleep(5)
land()
flush("Main_Log.txt")