import serial, binascii, sys, time

VOLMUTE = "\x08\x22\x02\x00\x00\x00\xd4"
serial.Serial(7,9600,timeout = 1).write(VOLMUTE)