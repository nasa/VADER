import serial, binascii, sys, time

#HDMI 2
WIDISWITCH = "\x20\x02\x01\x02\x47"
serial.Serial(6,9600,timeout = 1).write(WIDISWITCH)