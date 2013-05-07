import serial, binascii, sys, time

#HDMI 4 
ATVSWITCH = "\x20\x02\x01\x04\x9a"
serial.Serial(6,9600,timeout = 1).write(ATVSWITCH)
