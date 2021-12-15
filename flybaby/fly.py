#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from haversine import haversine
from mavsdk.camera import (CameraError, Mode, Option, Setting, PhotosRange)
from aioconsole import ainput
"""
camera_mode = Mode.PHOTO
current_settings = []
possible_setting_options = []"""

async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break


    #stjålet fra MAVSDK kamera eksempel
    """asyncio.ensure_future(observe_current_settings(drone))
    asyncio.ensure_future(observe_camera_mode(drone))
    asyncio.ensure_future(observe_possible_setting_options(drone))"""
    """try:
        await drone.camera.prepare()
        print(f" --> Succeeded")
    except CameraError as error:
        print("couldnt prepare")
        print(f" --> Failed with code: {error._result.result_str}")

    print(drone.camera.information())
    """
    try:
        await drone.camera.set_mode(Mode.PHOTO)
        print(f" --> Succeeded")
    except CameraError as error:
        print("couldnt set mode to photo")
        print(f" --> Failed with code: {error._result.result_str}")

    await asyncio.sleep(2)




    print("Taking a photos")
    try:
        await drone.camera.start_photo_interval(5.0)
    except CameraError as error:
        print("couldnt take foto")
        print(f"Couldn't take photo: {error._result.result}")

    try:
        await drone.camera.list_photos(PhotosRange(0))
    except CameraError as error:
        print(f"couldnt list fotos: {error._result.result}")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    home_position = drone.telemetry.home()
    print(home_position)
    """home_drone_lat = home_position.latitude_deg
    home_drone_long = home_position.longitude_deg
    home_alt = home_position.relaive_altitude_m
    """

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, 20m up within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await check_is_at_goal(0.0, 0.0, 5.0, drone)


"""
    for i in range(5):
        print("-- Go 50m North, 0m East, stay at 20m")
        await drone.offboard.set_position_ned(PositionNedYaw(50.0, 0.0, -20.0, 0.0))
        await asyncio.sleep(30)

        print("-- Go 0m North, 25m East, stay at 20m, turn to face east (hopefully)")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 25.0, -20.0, 90.0))
        await asyncio.sleep(30)

        print("-- Go 50m South, 0m East, stay at 20m, turn to face South")
        await drone.offboard.set_position_ned(PositionNedYaw(-50.0, 00.0, -20.0, 180.0))
        await asyncio.sleep(30)

        if (i != 4):
            print("-- Go 0m North, 25m East, stay at 20m, turn to face East.")
            await drone.offboard.set_position_ned(PositionNedYaw(0.0, 25.0, -20.0, 90.0))
            await asyncio.sleep(30)

    print("-- Go 50m South, 0m East, stay at 20m, turn to face South.")
    await drone.offboard.set_position_ned(PositionNedYaw(-50.0, 0.0, -20.0, 180.0))
    await asyncio.sleep(30)

    for i in range(5):
        print("-- Go 0m North, 25m East, stay at 20m.")
        await drone.offboard.set_position_ned(PositionNedYaw(-50.0, 0.0, -20.0, 0.0))
        await asyncio.sleep(30)

        print("-- Go 0m North, 25m West, stay at 20m, turn to face West (again hopefully)")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, -25.0, -20.0, 270.0))
        await asyncio.sleep(30)

        print("-- Go 50m North, 0m East, stay at 20m, turn to face South")
        await drone.offboard.set_position_ned(PositionNedYaw(50.0, 00.0, -20.0, 180.0))
        await asyncio.sleep(30)

        if (i != 4):
            print("-- Go 0m North, 25m West, stay at 20m, turn to face East")
            await drone.offboard.set_position_ned(PositionNedYaw(0.0, -25.0, -20.0, 90.0))
            await asyncio.sleep(30)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

"""


async def check_is_at_goal(goal_lat, goal_long, goal_alt, drone):
    async for position in drone.telemetry.position():
        curr_drone_lat = position.latitude_deg
        curr_drone_long = position.longitude_deg
        drone_alt = position.relative_altitude_m
        dist_to_goal = haversine((curr_drone_lat, curr_drone_long), (goal_lat, goal_long))/1000  # in meters

        """if dist_to_goal <= 1 and abs(drone_alt - goal_alt) <= 1:
            print("goal reached")
            return"""
        if abs(drone_alt - goal_alt) <= 0.5:
            print("goal reached")
            return



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
