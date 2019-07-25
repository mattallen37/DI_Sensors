#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for using the PCF8591 AD/DA converter

# !!! WARNING !!!
# This example program is untested. Currently this is only intended to be used as a starting point.

from __future__ import print_function
from __future__ import division

import time
from di_sensors import PCF8591

AD_DA = PCF8591.PCF8591()

while True:
    # read ADC channel 0
    adc = AD_DA.get_channel(0)

    # print the ADC value
    print("ADC: %3d" % adc)

    # set the DAC value to the inverse of the adc value
    AD_DA.set_output((255 - adc))

    time.sleep(0.02) # slow down
