import serial, binascii, sys, time

POWERON = "\x08\x22\x00\x00\x00\x02\xd4"
serial.Serial(7,9600,timeout = 1).write(POWERON)