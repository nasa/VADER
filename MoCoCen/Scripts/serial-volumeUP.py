import serial, binascii, sys, time

VOLUP = "\x08\x22\x01\x00\x01\x00\xd4"
#COM port varies on USB port.
serial.Serial(7,9600,timeout = 1).write(VOLUP)
