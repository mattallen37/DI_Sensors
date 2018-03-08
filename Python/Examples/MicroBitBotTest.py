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

mbb = MicroBitBot("RPI_1")

print("Manufacturer: " + mbb.get_manufacturer())
print("Board: " + mbb.get_board())
print("Firmware Version: %d" % mbb.get_version_firmware())
print("5v voltage: %1.4f" % mbb.get_voltage_5v())
print("Battery Voltage: %1.4f" % mbb.get_voltage_battery())

mbb.set_motor_power(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, mbb.MOTOR_FLOAT)

time.sleep(0.01)

mbb.offset_motor_encoder(mbb.MOTOR_LEFT, mbb.get_motor_encoder(mbb.MOTOR_LEFT))
mbb.offset_motor_encoder(mbb.MOTOR_RIGHT, mbb.get_motor_encoder(mbb.MOTOR_RIGHT))

#mbb.set_motor_power(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, 50)
mbb.set_motor_position(mbb.MOTOR_RIGHT, 200)
mbb.set_motor_limits(mbb.MOTOR_LEFT, power = 50, dps = 175)
count = 0

while True:
    #print("Encoder Left: %6d  Right %6d" % (mbb.get_motor_encoder(mbb.MOTOR_LEFT), mbb.get_motor_encoder(mbb.MOTOR_RIGHT)))
    LineSensors = mbb.get_line_sensors()
    MotorStatusLeftFlags, MotorStatusLeftPower, MotorStatusLeftEncoder, MotorStatusLeftSpeed = mbb.get_motor_status(mbb.MOTOR_LEFT)
    MotorStatusRightFlags, MotorStatusRightPower, MotorStatusRightEncoder, MotorStatusRightSpeed = mbb.get_motor_status(mbb.MOTOR_RIGHT)
    print("5v: %6.3fv  Battery: %6.3fv  Line Sensors: %.2f %.2f %.2f %.2f %.2f  Motor Status Bits: %.2X %.2X  Power: %4d %4d  Encoder: %6d %6d  Speed: %5d %5d" % (mbb.get_voltage_5v(), mbb.get_voltage_battery(),
        LineSensors[0], LineSensors[1], LineSensors[2], LineSensors[3], LineSensors[4],
        MotorStatusLeftFlags, MotorStatusRightFlags, MotorStatusLeftPower, MotorStatusRightPower, MotorStatusLeftEncoder, MotorStatusRightEncoder, MotorStatusLeftSpeed, MotorStatusRightSpeed))
    
    
    #mbb.set_motor_position(mbb.MOTOR_LEFT, count * 5)
    
    if count % 25 == 24:
        if count % 50 == 24:
            mbb.set_motor_position(mbb.MOTOR_LEFT, 90)
            mbb.set_motor_dps(mbb.MOTOR_RIGHT, 20)
        else:
            mbb.set_motor_position(mbb.MOTOR_LEFT, -90)
            mbb.set_motor_dps(mbb.MOTOR_RIGHT, -40)
    
#    if count == 5:
#        mbb.set_motor_power(mbb.MOTOR_LEFT + mbb.MOTOR_RIGHT, mbb.MOTOR_FLOAT)
    
    count += 1
    time.sleep(0.1)
