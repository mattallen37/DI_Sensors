#!/usr/bin/env python
#
# https://www.dexterindustries.com/
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries MicroBitBot

from __future__ import print_function
from __future__ import division

import time
from di_sensors.micro_bit_bot import MicroBitBot

try:
    mbb = MicroBitBot("RPI_1SW")#"GPG3_AD1")

    print("Manufacturer: " + mbb.get_manufacturer())
    print("Board: " + mbb.get_board())
    print("Firmware Version: %d" % mbb.get_version_firmware())
    print("Battery Voltage: %1.4f" % mbb.get_voltage_battery())
    print("Rail Voltage: %1.4f" % mbb.get_voltage_rail())

    mbb.set_motor_powers(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, mbb.MOTOR_FLOAT)

    time.sleep(0.01)

    mbb.set_motor_powers(50, 50)
    count = 0

    while True:
        #print("Encoder Left: %6d  Right %6d" % (mbb.get_motor_encoder(mbb.MOTOR_LEFT), mbb.get_motor_encoder(mbb.MOTOR_RIGHT)))
        LineSensors = mbb.get_line_sensors()
        LightSensors = mbb.get_light_sensors()
        MotorStatusLeftFlags, MotorStatusLeftPower = mbb.get_motor_status(mbb.MOTOR_LEFT)
        MotorStatusRightFlags, MotorStatusRightPower = mbb.get_motor_status(mbb.MOTOR_RIGHT)
        print("Battery: %6.3fv  Rail: %6.3fv  Line Sensors: %.2f %.2f  Light Sensors: %.2f %.2f  Motor Status Bits: %.2X %.2X  Power: %4d %4d" % (
            mbb.get_voltage_battery(),
            mbb.get_voltage_rail(),
            LineSensors[0], LineSensors[1],
            LightSensors[0], LightSensors[1],
            MotorStatusLeftFlags, MotorStatusRightFlags,
            MotorStatusLeftPower, MotorStatusRightPower))


        #mbb.set_motor_position(mbb.MOTOR_LEFT, count * 5)

        if count % 25 == 24:
            if count % 50 == 24:
                mbb.set_motor_powers(25, -50)
            else:
                mbb.set_motor_powers(-50, 25)

    #    if count == 5:
    #        mbb.set_motor_power(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, mbb.MOTOR_FLOAT)

        count += 1
        time.sleep(0.1)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    mbb.set_motor_powers(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, mbb.MOTOR_FLOAT)
