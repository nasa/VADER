import serial, binascii, sys, time

#HDMI 1
VADERSWITCH = "\x20\x02\x01\x01\xa5"
serial.Serial(6,9600,timeout = 1).write(VADERSWITCH)
