import serial, binascii, sys, time

#HDMI 6
MULTIDISPLAYSWITCH = "\x20\x02\x01\x06\x26"
serial.Serial(6,9600,timeout = 1).write(MULTIDISPLAYSWITCH)