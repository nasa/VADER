import serial, binascii, sys, time
dispNum = sys.argv[1]

VOLDOWN = "\x08\x22\x01\x00\x02\x00\xd3"
RECEIVERVOLDOWN = "\x4d\x56\x44\x4f\x57\x4e\x0d"
if dispNum == '1':
	serial.Serial(3,9600,timeout = 1).write(VOLDOWN)
elif dispNum == '2':
	serial.Serial(4,9600,timeout = 1).write(VOLDOWN)
elif dispNum == '3':
	serial.Serial(3,9600,timeout = 1).write(VOLDOWN)
	serial.Serial(4,9600,timeout = 1).write(VOLDOWN)
	serial.Serial(6,9600,timeout = 1).write(RECEIVERVOLDOWN)


#VOLDOWN = "\x08\x22\x01\x00\x02\x00\xd3"
#serial.Serial(3,9600,timeout = 1).write(VOLDOWN)
#serial.Serial(4,9600,timeout = 1).write(VOLDOWN)