import serial, binascii, sys, time

VOLDOWN = "\x08\x22\x01\x00\x02\x00\xd3"
serial.Serial(7,9600,timeout = 1).write(VOLDOWN)