import serial, binascii, sys, time

#HDMI 7
INPUT7SWITCH = "\x20\x02\x01\x07\x78"
serial.Serial(6,9600,timeout = 1).write(INPUT7SWITCH)