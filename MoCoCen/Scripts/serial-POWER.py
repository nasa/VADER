import serial, binascii, sys, time

POWERTOGGLE = "\x08\x22\x00\x00\x00\x00\xd6"
serial.Serial(7,9600,timeout = 1).write(POWERTOGGLE)