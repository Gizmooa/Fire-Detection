#!/usr/bin/env python3
################################################################################################
# @File DroneKitPX4.py
# Example usage of DroneKit with PX4
#
# @author Sander Smeets <sander@droneslab.com>
#
# Code partly based on DroneKit (c) Copyright 2015-2016, 3D Robotics.
################################################################################################

# Import DroneKit-Python

from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

class DroneMission:
	connection_string = None
	MAV_MODE_AUTO = None
	vehicle = None
	home_position_set = False

	def __init__(self, connection_string = '127.0.0.1:14540', MAV_MODE = 4):
		self.connection_string = connection_string
		self. MAV_MODE_AUTO = MAV_MODE

		# Parse connection argument (DETTE er vel ligemeget?)
		parser = argparse.ArgumentParser()
		parser.add_argument("-c", "--connect", help="connection string")
		args = parser.parse_args()

		if args.connect:
			self.connection_string = args.connect

		################################################################################################
		# Init
		################################################################################################

		# Connect to the Vehicle
		print("Connecting")
		self.vehicle = connect(connection_string, wait_ready=True)

	def PX4setMode(self, mavMode):
		self.vehicle._master.mav.command_long_send(self.vehicle._master.target_system, self.vehicle._master.target_component,
												   mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
												   mavMode,
												   0, 0, 0, 0, 0, 0)



	def get_location_offset_meters(self, original_location, dNorth, dEast, alt):
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
		#Coordinate offsets in radians
		dLat = dNorth/earth_radius
		dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

		#New position in decimal degrees
		newlat = original_location.lat + (dLat * 180/math.pi)
		newlon = original_location.lon + (dLon * 180/math.pi)
		return LocationGlobal(newlat, newlon,original_location.alt+alt)





	################################################################################################
	# Listeners
	################################################################################################

	#Create a message listener for home position fix
	@vehicle.on_message('HOME_POSITION')
	def listener(self, name, home_position):
		self.home_position_set = True

	def start_mission(self):
		while not self.home_position_set:
			print("Waiting for home position...")
			time.sleep(1)

		# Change to AUTO mode
		self.PX4setMode(self.MAV_MODE_AUTO)
		time.sleep(1)

		# Load commands
		cmds = self.vehicle.commands
		cmds.clear()

		home = self.vehicle.location.global_relative_frame

		# takeoff to 10 meters
		wp = self.get_location_offset_meters(home, 0, 0, 75);  # Height depends on height of trees in the area
		cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1,
					  0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
		cmds.add(cmd)

		for i in range(5):
			# move 50 meters north
			wp = self.get_location_offset_meters(wp, 50, 0, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			# move 25 meters east
			wp = self.get_location_offset_meters(wp, 0, 25, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			# move 50 meters south
			wp = self.get_location_offset_meters(wp, -50, 0, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			if (i != 4):
				# move 25 meters east
				wp = self.get_location_offset_meters(wp, 0, 25, 0);
				cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
							  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
				cmds.add(cmd)

		# move 50 meters south
		wp = self.get_location_offset_meters(wp, -25, 0, 0);
		cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,
					  1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
		cmds.add(cmd)

		for i in range(5):
			# move 50 meters south
			wp = self.get_location_offset_meters(wp, -50, 0, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			# move 25 meters west
			wp = self.get_location_offset_meters(wp, 0, -25, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			# move 50 meters north
			wp = self.get_location_offset_meters(wp, 50, 0, 0);
			cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
						  0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
			cmds.add(cmd)

			if (i != 4):
				# move 25 meters west
				wp = self.get_location_offset_meters(wp, 0, -25, 0);
				cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
							  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
				cmds.add(cmd)

		# land
		wp = self.get_location_offset_meters(home, 0, 0, 75);
		cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0,
					  0, 0, 0, wp.lat, wp.lon, wp.alt)
		cmds.add(cmd)

		# Upload mission
		cmds.upload()
		time.sleep(2)

		# Arm vehicle
		self.vehicle.armed = True

		# monitor mission execution
		nextwaypoint = self.vehicle.commands.next
		while nextwaypoint < len(self.vehicle.commands):
			if self.vehicle.commands.next > nextwaypoint:
				display_seq = self.vehicle.commands.next + 1
				print("Moving to waypoint %s" % display_seq)
				nextwaypoint = self.vehicle.commands.next
			time.sleep(1)

		# wait for the vehicle to land
		while self.vehicle.commands.next > 0:
			time.sleep(1)

		# Disarm vehicle
		self.vehicle.armed = False
		time.sleep(1)

		# Close vehicle object before exiting script
		self.vehicle.close()
		time.sleep(1)