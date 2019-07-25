# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the PCF8591 I2C AD/DA converter

# !!! WARNING !!!
# These drivers are untested. Currently this is only intended to be used as a starting point.

from __future__ import print_function
from __future__ import division

import di_i2c


class PCF8591(object):
    """Drivers for PCF8591 AD/DA converter"""

    def __init__(self, address = 0x48, bus = "RPI_1SW"):
        """Initialize the I2C analog interface

        Keyword arguments:
        address (default 0x48) -- The I2C address
        bus (default RPI_1SW) -- The I2C bus"""
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = address)

    def get_channel(self, channel):
        """Read an analog input ADC channel

        Keyword arguments:
        channel -- the channel to read

        Returns the 8-bit ADC value for the channel"""

        # set the register to read from
        if channel == 0:
            self.i2c_bus.write_8(0x40)
        if channel == 1:
            self.i2c_bus.write_8(0x41)
        if channel == 2:
            self.i2c_bus.write_8(0x42)
        if channel == 3:
            self.i2c_bus.write_8(0x43)

        self.i2c_bus.read_8() # dummy read to start conversion

        return self.i2c_bus.read_8() # return the ADC value

    def set_output(self, value):
        """Set the analog output

        Keyword arguments:
        value -- the 8-bit DAC value to set"""
        self.i2c_bus.write_reg_8(0x40, value)
