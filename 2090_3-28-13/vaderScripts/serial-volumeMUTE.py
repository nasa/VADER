import serial, binascii, sys, time
dispNum = sys.argv[1]

VOLMUTE = "\x08\x22\x02\x00\x00\x00\xd4"
if dispNum == '1':
	serial.Serial(3,9600,timeout = 1).write(VOLMUTE)
elif dispNum == '2':
	serial.Serial(4,9600,timeout = 1).write(VOLMUTE)
elif dispNum == '3':
	serial.Serial(3,9600,timeout = 1).write(VOLMUTE)
	serial.Serial(4,9600,timeout = 1).write(VOLMUTE)


#VOLMUTE = "\x08\x22\x02\x00\x00\x00\xd4"
#serial.Serial(3,9600,timeout = 1).write(VOLMUTE)
#serial.Serial(4,9600,timeout = 1).write(VOLMUTE)