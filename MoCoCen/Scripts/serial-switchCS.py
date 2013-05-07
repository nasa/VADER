import serial, binascii, sys, time

#HDMI 5
CLICKSHARESWITCH = "\x20\x02\x01\x05\xc4"
serial.Serial(6,9600,timeout = 1).write(CLICKSHARESWITCH)