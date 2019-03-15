#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Line Follower sensor

from __future__ import print_function
from __future__ import division

import time
from di_sensors import line_follower

print("Example program for reading a Dexter Industries Line Follower sensor on an I2C port")

lf = line_follower.LineFollower()

print("Manufacturer     : %s" % lf.get_manufacturer())
print("Name             : %s" % lf.get_board())
print("Firmware Version : %d" % lf.get_version_firmware())

while True:
    # Read the line follower sensor values
    values = lf.read_sensors()
    str = ""
    for v in range(len(values)):
        str += "%.3f " % values[v]
    print(str)

    time.sleep(0.1)
