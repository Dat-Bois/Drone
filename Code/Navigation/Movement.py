from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
from logger import log, flush


def flush_log(fileName):
    flush(fileName)

def initialize(port = '/dev/ttyACM0'):
    global vehicle
    vehicle = connect(port, wait_ready=True, baud=921600)

def initialization_check():
    print ("Autopilot Firmware version: %s" % vehicle.version)
    log("Autopilot Firmware version: " + str(vehicle.version))
    #print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
    #print "Global Location: %s" % vehicle.location.global_frame
    #print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    #print "Local Location: %s" % vehicle.location.local_frame    #NED
    #print "Attitude: %s" % vehicle.attitude
    #print "Velocity: %s" % vehicle.velocity
    print ("GPS: %s" % vehicle.gps_0)
    log("GPS: " + str(vehicle.gps_0))
    #print "Groundspeed: %s" % vehicle.groundspeed
    #print "Airspeed: %s" % vehicle.airspeed
    #print "Gimbal status: %s" % vehicle.gimbal
    print ("Battery: %s" % vehicle.battery)
    log("Battery: " + str(vehicle.battery))
    #print "EKF OK?: %s" % vehicle.ekf_ok
    #print "Last Heartbeat: %s" % vehicle.last_heartbeat
    #print "Rangefinder: %s" % vehicle.rangefinder
    #print "Rangefinder distance: %s" % vehicle.rangefinder.distance
    #print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    #print "Heading: %s" % vehicle.heading
    print ("Is Armable?: %s" % vehicle.is_armable)
    log("Is Armable?: " + str(vehicle.is_armable))
    print ("System status: %s" % vehicle.system_status.state)
    log("System status: " + str(vehicle.system_status.state))
    print ("Mode: %s" % vehicle.mode.name)    # settable
    log("Mode: " + str(vehicle.mode.name))
    print ("Armed: %s" % vehicle.armed)    # settable
    log("Armed: " + str(vehicle.armed))

def arm_and_takeoff(targetAltitude):
    print("Arming Motors...")
    log("Arming Motors...")
    #vehicle.mode = "GUIDED"
    vehicle.mode = VehicleMode("GUIDED")
    print ("Mode: %s" % vehicle.mode.name)    # settable
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
        #print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
        if (vehicle.location.global_relative_frame.alt >= targetAltitude*0.95):
            print("Reached Target Altitude")
            log("Reached Target Altitude")
            break
        time.sleep(1)

def land():
    print("landing now!")
    #vehicle.mode = "LAND"
    vehicle.mode = VehicleMode("LAND")

def setAlt(targetAltitude):
    loc = vehicle.LocationGlobalRelative
    loc.alt = targetAltitude
    vehicle.simple_goto(loc)
    if (vehicle.LocationGlobalRelative.alt <= targetAltitude):
        while True:
            #print (" Altitude: ", vehicle.location.global_relative_frame.alt)
            log("Altitude: " + str(vehicle.location.global_relative_frame.alt))
            if (vehicle.location.global_relative_frame.alt >= targetAltitude*0.95):
                print("Reached Target Altitude")
                log("Reached Target Altitude")
                return
            time.sleep(1)
    if (vehicle.LocationGlobalRelative.alt >= targetAltitude):
        while True:
            #print (" Altitude: ", vehicle.location.global_relative_frame.alt)
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

def changeYaw(heading, rotate):
    log("Moving yaw: " + str(heading) + " degrees "+str(rotate)+" (-1 ccw & 1 cw)")
    msg = vehicle.message_factory.command_long_encode(0, 0, mavutil.mavlink.MAV_CMD_CONDITION_YAW, 0, heading, 0, rotate, 1, 0, 0, 0) #Look at movement.py for parameter def.
    # send command to vehicle
    vehicle.send_mavlink(msg)
    log("Sent yaw command")
    current_heading = int((int(vehicle.attitude.yaw)*(180/3.14159265359)))
    target_heading =  current_heading + (heading * rotate)
    if target_heading < 0:
        target_heading = 360 + target_heading
    if target_heading > 360:
        target_heading = target_heading - 360
    while target_heading != current_heading:
        current_heading = int((int(vehicle.attitude.yaw)*(180/3.14159265359))) #this makes it wait until the manuver is complete and not any longer
        log("Current: " + str(current_heading) + "  Target: " + str(target_heading))
    log("Moved to position")


def groundSpeed(speed):
    vehicle.groundspeed = speed

def send_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    velocity_x is backward/forward and velocity_y is left/right (m/s)
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 0b0000111111000111, 0, 0, 0, velocity_x, velocity_y, velocity_z, 0, 0, 0,0, 0)
    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
        log("Sent move command: x:" + str(velocity_x) + '  y:' + str(velocity_y) + '  z:' + str(velocity_z))