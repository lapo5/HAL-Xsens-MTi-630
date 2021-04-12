#!/usr/bin/env python
import serial
import struct
import sys
import getopt
import time
import glob
import re
import pprint
import mtdevice
from mtnode import XSensDriver

from mtdef import MID, OutputMode, OutputSettings, MTException, Baudrates, \
    XDIGroup, getMIDName, DeviceState, DeprecatedMID, MTErrorMessage, \
    MTTimeoutException

port = '/dev/ttyUSB0'
baudrate = 115200

timeout=0.002
timeout = 100*timeout

try:
    device = serial.Serial(port, baudrate, timeout=timeout,
                                writeTimeout=timeout)
except IOError:
    # FIXME with pyserial3 we might need some specific flags
    device = serial.Serial(port, baudrate, timeout=timeout,
                                writeTimeout=timeout, rtscts=True,
                                dsrdtr=True)

driver = XSensDriver()
#driver.spin()