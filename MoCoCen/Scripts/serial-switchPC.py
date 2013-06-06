import serial, binascii, sys, time

PCSWITCH = "\x08\x22\x0a\x00\x04\x00\xc8"
serial.Serial(7,9600,timeout = 1).write(PCSWITCH)