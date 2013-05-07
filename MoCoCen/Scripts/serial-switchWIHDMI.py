import serial, binascii, sys, time

#HDMI 3
WIHDMISWITCH = "\x20\x02\x01\x03\x19"
serial.Serial(6,9600,timeout = 1).write(WIHDMISWITCH)