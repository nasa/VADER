import serial, binascii, sys, time

#HDMI 8
INPUT8SWITCH = "\x20\x02\x01\x08\x39"
serial.Serial(6,9600,timeout = 1).write(INPUT8SWITCH)