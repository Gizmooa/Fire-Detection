#!/usr/bin/env python3
################################################################################################
# @File droneMission.py
# Example usage of DroneKit with PX4, modified further by owner and collaborators of this repository.
#
# @author Sander Smeets <sander@droneslab.com>
#
# Code partly based on DroneKit (c) Copyright 2015-2016, 3D Robotics.
################################################################################################

from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, argparse, math

vehicle = None
home = None
mission_is_done = False

################################################################################################
# Settings
################################################################################################

connection_string       = '127.0.0.1:14540'
MAV_MODE_AUTO   = 4
# https://github.com/PX4/PX4-Autopilot/blob/master/Tools/mavlink_px4.py


# Parse connection argument
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--connect", help="connection string")
parser.add_argument("-he",'--height', type=int,
                    help='Option to change the default height to something else.')
args = parser.parse_args()

if args.connect:
    connection_string = args.connect


################################################################################################
# Init
################################################################################################

# Connect to the Vehicle
print("Connecting")
vehicle = connect(connection_string, wait_ready=True)


################################################################################################
# Listeners
################################################################################################

home_position_set = False


# Create a message listener for home position fix
@vehicle.on_message('HOME_POSITION')
def listener(self, name, home_position):
    global home_position_set
    home_position_set = True

def PX4setMode(mavMode):
    global vehicle
    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
                                               mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                               mavMode,
                                               0, 0, 0, 0, 0, 0)



def get_location_offset_meters(original_location, dNorth, dEast, alt):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    # Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    # New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt+alt)


def start_mission():
    global vehicle
    global home
    global home_position_set
    global args
    global mission_is_done

    ################################################################################################
    # Start mission example
    ################################################################################################

    while not home_position_set:
        print ("Waiting for home position...")
        time.sleep(3)

    # Change to AUTO mode
    PX4setMode(MAV_MODE_AUTO)
    time.sleep(1)

    # Load commands
    cmds = vehicle.commands
    cmds.clear()

    home = vehicle.location.global_relative_frame

    height = 50
    if (args.height != None and height > 0):
        print(f"Changing default height from 50 to {args.height}")
        height = args.height

    # If no argument for height have been given, take off to 50 meters. Otherwise to the specified height.
    wp = get_location_offset_meters(home, 0, 0, height); #Height depends on height of trees in the area
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)

    for i in range (5):
        # move 50 meters north
        wp = get_location_offset_meters(wp, 50, 0, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)

        # move 25 meters east
        wp = get_location_offset_meters(wp, 0, 25, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)

        # move 50 meters south
        wp = get_location_offset_meters(wp, -50, 0, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)

        if (i != 4):
            # move 25 meters east
            wp = get_location_offset_meters(wp, 0, 25, 0);
            cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
            cmds.add(cmd)

    # move 25 meters south
    wp = get_location_offset_meters(wp, -25, 0, 0);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)

    for i in range (5):
        # move 50 meters south
        wp = get_location_offset_meters(wp, -50, 0, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)

        # move 25 meters west
        wp = get_location_offset_meters(wp, 0, -25, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)

        # move 50 meters north
        wp = get_location_offset_meters(wp, 50, 0, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)


        if (i != 4):
            # move 25 meters west
            wp = get_location_offset_meters(wp, 0, -25, 0);
            cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
            cmds.add(cmd)

    # land
    wp = get_location_offset_meters(home, 0, 0, 75);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)

    # Upload mission
    cmds.upload()
    time.sleep(2)

    # Arm vehicle
    vehicle.armed = True

    # monitor mission execution
    nextwaypoint = vehicle.commands.next
    print(f"Moving to waypoint {nextwaypoint+1}")
    while nextwaypoint < len(vehicle.commands):
        if vehicle.commands.next > nextwaypoint:
            display_seq = vehicle.commands.next+1
            print("\nMoving to waypoint %s" % display_seq)
            nextwaypoint = vehicle.commands.next
        time.sleep(1)

    # wait for the vehicle to land
    while vehicle.commands.next > 0:
        time.sleep(1)


    # Disarm vehicle
    vehicle.armed = False
    mission_is_done = True
    time.sleep(1)

    # Close vehicle object before exiting script
    vehicle.close()
    time.sleep(1)
