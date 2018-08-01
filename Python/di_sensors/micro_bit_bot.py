# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for testing the Dexter Industries MicroBitBot

from __future__ import print_function
from __future__ import division

from di_sensors import dexter_i2c

import math       # import math for math.pi constant
import time


class Enumeration(object):
    def __init__(self, names):  # or *names, with no .split()
        number = 0
        for line, name in enumerate(names.split('\n')):
            if name.find(",") >= 0:
                # strip out the spaces
                while(name.find(" ") != -1):
                    name = name[:name.find(" ")] + name[(name.find(" ") + 1):]

                # strip out the commas
                while(name.find(",") != -1):
                    name = name[:name.find(",")] + name[(name.find(",") + 1):]

                # if the value was specified
                if(name.find("=") != -1):
                    number = int(float(name[(name.find("=") + 1):]))
                    name = name[:name.find("=")]

                # optionally print to confirm that it's working correctly
                #print "%40s has a value of %d" % (name, number)

                setattr(self, name, number)
                number = number + 1


class MicroBitBot():
    """Dexter Industries drivers for testing MicroBitBot"""

    I2C_COMMAND = Enumeration("""
        GET_FIRMWARE_VERSION = 1,
        GET_MANUFACTURER,
        GET_BOARD,
        GET_VOLTAGE_BATTERY,
        GET_LINE_SENSORS,
        GET_LIGHT_SENSORS,
        GET_MOTOR_STATUS_RIGHT,
        GET_MOTOR_STATUS_LEFT,
        SET_MOTOR_POWER,
        SET_MOTOR_POWERS,
        GET_VOLTAGE_RAIL,
    """)

    MOTOR_LEFT  = 0x01
    MOTOR_RIGHT = 0x02

    MOTOR_FLOAT = -128

    def __init__(self, bus):
        self.i2c_bus = dexter_i2c.Dexter_I2C(bus = bus, address = 0x04)

    def get_manufacturer(self):
        array = self.i2c_bus.read_list(self.I2C_COMMAND.GET_MANUFACTURER, 20)

        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name

    def get_board(self):
        array = self.i2c_bus.read_list(self.I2C_COMMAND.GET_BOARD, 20)

        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name

    def get_version_firmware(self):
        return self.i2c_bus.read_16(self.I2C_COMMAND.GET_FIRMWARE_VERSION)

    def get_voltage_battery(self):
        return (self.i2c_bus.read_16(self.I2C_COMMAND.GET_VOLTAGE_BATTERY) / 1000)

    def get_voltage_rail(self):
        return (self.i2c_bus.read_16(self.I2C_COMMAND.GET_VOLTAGE_RAIL) / 1000)

    def __get_sensors__(self, reg):
        array = self.i2c_bus.read_list(reg, 3)

        for s in range(2):
            array[s] <<= 2
            array[s] |= (((array[2] << (s * 2)) & 0xC0) >> 6)
            array[s] = (1023 - array[s]) / 1023.0 # invert and scale to a range of 0 to 1
        return array[:2] # return the 2 sensor values

    def get_line_sensors(self):
        return self.__get_sensors__(self.I2C_COMMAND.GET_LINE_SENSORS)

    def get_light_sensors(self):
        return self.__get_sensors__(self.I2C_COMMAND.GET_LIGHT_SENSORS)

    def set_motor_power(self, port, power):
        outArray = [port, (int(power) & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_POWER, outArray)

    def set_motor_powers(self, powerRight, powerLeft):
        outArray = [(int(powerRight) & 0xFF), (int(powerLeft) & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_POWERS, outArray)

    def get_motor_status(self, port):
        if port == self.MOTOR_LEFT:
            message_type = self.I2C_COMMAND.GET_MOTOR_STATUS_LEFT
        elif port == self.MOTOR_RIGHT:
            message_type = self.I2C_COMMAND.GET_MOTOR_STATUS_RIGHT

        array = self.i2c_bus.read_list(message_type, 2)

        flags = array[0]
        power = array[1]
        if power & 0x80:
            power = power - 0x100

        return [flags, power]

    def reset_all(self):
        # Turn off the motors
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, self.MOTOR_FLOAT)
