#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    drone.action.arm()

    # await drone.action.set_takeoff_altitude(75)

    print("-- Setting initial setpoint")
    drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, 75m up within local coordinate system")
    drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -20.0, 0.0))
    # await asyncio.sleep(40)

    for i in range(5):
        print("-- Go 5m North, 0m East, -5m Down within local coordinate system, turn to face East")
        drone.offboard.set_position_ned(PositionNedYaw(50.0, 0.0, -20.0, 0.0))
        # await asyncio.sleep(30)

        print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
        drone.offboard.set_position_ned(PositionNedYaw(0.0, 25.0, -20.0, 90.0))
        # await asyncio.sleep(30)

        print("-- Go 0m North, 10m East, 0m Down within local coordinate system, turn to face South")
        drone.offboard.set_position_ned(PositionNedYaw(-50.0, 00.0, -20.0, 180.0))
        # await asyncio.sleep(30)

        if (i != 4):
            print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
            drone.offboard.set_position_ned(PositionNedYaw(0.0, 25.0, -20.0, 90.0))
            # await asyncio.sleep(30)

    drone.offboard.set_position_ned(PositionNedYaw(-50.0, 0.0, -20.0, 180.0))
    # await asyncio.sleep(30)

    for i in range(5):
        print("-- Go 5m North, 0m East, -5m Down within local coordinate system, turn to face East")
        drone.offboard.set_position_ned(PositionNedYaw(-50.0, 0.0, -20.0, 0.0))
        # await asyncio.sleep(30)

        print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
        drone.offboard.set_position_ned(PositionNedYaw(0.0, -25.0, -20.0, 90.0))
        # await asyncio.sleep(30)

        print("-- Go 0m North, 10m East, 0m Down within local coordinate system, turn to face South")
        drone.offboard.set_position_ned(PositionNedYaw(50.0, 00.0, -20.0, 180.0))
        # await asyncio.sleep(30)

        if (i != 4):
            print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
            await drone.offboard.set_position_ned(PositionNedYaw(0.0, -25.0, -20.0, 90.0))
            # await asyncio.sleep(30)

    print("-- Stopping offboard")
    try:
        drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
# run()