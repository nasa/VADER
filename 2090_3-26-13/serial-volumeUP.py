import serial, binascii, sys, time
dispNum = sys.argv[1]

VOLUP = "\x08\x22\x01\x00\x01\x00\xd4"
if dispNum == '1':
	serial.Serial(3,9600,timeout = 1).write(VOLUP)
elif dispNum == '2':
	serial.Serial(4,9600,timeout = 1).write(VOLUP)
elif dispNum == '3':
	serial.Serial(3,9600,timeout = 1).write(VOLUP)
	serial.Serial(4,9600,timeout = 1).write(VOLUP)

#VOLUP = "\x08\x22\x01\x00\x01\x00\xd4"
#VOLUP = "$08,$22,$01,$00,$01,$00,$d4"
#COM port varies on USB port.
#serial.Serial(3,9600,timeout = 1).write(VOLUP)
#serial.Serial(4,9600,timeout = 1).write(VOLUP)