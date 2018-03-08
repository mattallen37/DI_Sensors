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
    WHEEL_BASE_WIDTH         = 108  # distance (mm) from left wheel to right wheel. Will need to be adjusted.
    WHEEL_DIAMETER           = 66.5 # wheel diameter (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # The circumference of the circle the wheels will trace while turning (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # The circumference of the wheels (mm)

    MOTOR_GEAR_RATIO           = 120 # Motor gear ratio
    ENCODER_TICKS_PER_ROTATION = 6   # Encoder ticks per motor rotation (number of magnet positions)
    MOTOR_TICKS_PER_DEGREE = ((MOTOR_GEAR_RATIO * ENCODER_TICKS_PER_ROTATION) / 360.0) # encoder ticks per output shaft rotation degree
    
    I2C_COMMAND = Enumeration("""
        GET_FIRMWARE_VERSION = 1,
        GET_MANUFACTURER,
        GET_BOARD,
        GET_VOLTAGE_5V,
        GET_VOLTAGE_BATTERY,
        GET_LINE_SENSORS,
        GET_ENCODER_LEFT,
        GET_ENCODER_RIGHT,
        GET_MOTOR_STATUS_LEFT,
        GET_MOTOR_STATUS_RIGHT,
        SET_MOTOR_ENCODER_OFFSET,
        SET_MOTOR_POWER,
        SET_MOTOR_TARGET_POSITION,
        SET_MOTOR_TARGET_DPS,
        SET_MOTOR_LIMITS,
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
        self.i2c_bus.write_8(self.I2C_COMMAND.GET_FIRMWARE_VERSION)
        return self.i2c_bus.read_16()
    
    def get_voltage_5v(self):
        self.i2c_bus.write_8(self.I2C_COMMAND.GET_VOLTAGE_5V)
        return (self.i2c_bus.read_16() / 1000)
    
    def get_voltage_battery(self):
        self.i2c_bus.write_8(self.I2C_COMMAND.GET_VOLTAGE_BATTERY)
        return (self.i2c_bus.read_16() / 1000)
    
    def get_line_sensors(self):
        array = self.i2c_bus.read_list(self.I2C_COMMAND.GET_LINE_SENSORS, 7)
        
        for s in range(5):
            array[s] <<= 2
            array[s] |= (((array[5 + int(s / 4)] << ((s % 4) * 2)) & 0xC0) >> 6)
            array[s] = (1023 - array[s]) / 1023.0 # invert and scale to a range of 0 to 1
        return array[:5] # return the 5 sensor values
    
    def set_motor_power(self, port, power):
        outArray = [port, int(power)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_POWER, outArray)
    
    def set_motor_position(self, port, position):
        position = int(position * self.MOTOR_TICKS_PER_DEGREE)
        outArray = [int(port), ((position >> 24) & 0xFF), ((position >> 16) & 0xFF), ((position >> 8) & 0xFF), (position & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_TARGET_POSITION, outArray)
    
    def set_motor_dps(self, port, dps):
        dps = int(dps * self.MOTOR_TICKS_PER_DEGREE)
        outArray = [int(port), ((dps >> 8) & 0xFF), (dps & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_TARGET_DPS, outArray)
    
    def set_motor_limits(self, port, power = 0, dps = 0):
        dps = int(dps * self.MOTOR_TICKS_PER_DEGREE)
        outArray = [int(port), int(power), ((dps >> 8) & 0xFF), (dps & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_LIMITS, outArray)
    
    def get_motor_status(self, port):
        if port == self.MOTOR_LEFT:
            message_type = self.I2C_COMMAND.GET_MOTOR_STATUS_LEFT
        elif port == self.MOTOR_RIGHT:
            message_type = self.I2C_COMMAND.GET_MOTOR_STATUS_RIGHT
        
        array = self.i2c_bus.read_list(message_type, 8)
        
        flags = array[0]
        power = array[1]
        if power & 0x80:
            power = power - 0x100
        
        encoder = int((array[2] << 24) | (array[3] << 16) | (array[4] << 8) | array[5])
        if encoder & 0x80000000:
            encoder = int(encoder - 0x100000000)
        
        dps = int((array[6] << 8) | array[7])
        if dps & 0x8000:
            dps = dps - 0x10000
        
        return [flags, power, int(encoder / self.MOTOR_TICKS_PER_DEGREE), int(dps / self.MOTOR_TICKS_PER_DEGREE)]
    
    def get_motor_encoder(self, port):
        if port == self.MOTOR_LEFT:
            message_type = self.I2C_COMMAND.GET_ENCODER_LEFT
        elif port == self.MOTOR_RIGHT:
            message_type = self.I2C_COMMAND.GET_ENCODER_RIGHT
        encoder = self.i2c_bus.read_32(reg = message_type, signed = True)
        return int(encoder / self.MOTOR_TICKS_PER_DEGREE)
    
    def offset_motor_encoder(self, port, offset):
        offset = int(offset * self.MOTOR_TICKS_PER_DEGREE)
        outArray = [int(port), ((offset >> 24) & 0xFF), ((offset >> 16) & 0xFF), ((offset >> 8) & 0xFF), (offset & 0xFF)]
        self.i2c_bus.write_reg_list(self.I2C_COMMAND.SET_MOTOR_ENCODER_OFFSET, outArray)
    
    def reset_all(self):
        # Turn off the motors
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, self.MOTOR_FLOAT)
        
        # Reset the motor limits
        self.set_motor_limits(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0, 0)
