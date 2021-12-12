#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, 20m up within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -20.0, 0.0))
    await asyncio.sleep(40)

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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
