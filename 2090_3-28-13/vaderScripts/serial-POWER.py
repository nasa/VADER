import serial, binascii, sys, time
dispNum = sys.argv[1]

POWERTOGGLE = "\x08\x22\x00\x00\x00\x00\xd6"
#RECEIVERPOWERSTANDBY = "\x50\x57\x53\x54\x41\x4e\x44\x42\x59\x0d"
#RECEIVERPOWERON = "\x50\x57\x4f\x4e\x0d"
if dispNum == '1':
	serial.Serial(3,9600,timeout = 1).write(POWERTOGGLE)
elif dispNum == '2':
	serial.Serial(4,9600,timeout = 1).write(POWERTOGGLE)
elif dispNum == '3':
	serial.Serial(3,9600,timeout = 1).write(POWERTOGGLE)
	serial.Serial(4,9600,timeout = 1).write(POWERTOGGLE)

#POWERTOGGLE = "\x08\x22\x00\x00\x00\x00\xd6"
#serial.Serial(3,9600,timeout = 1).write(POWERTOGGLE)
#serial.Serial(4,9600,timeout = 1).write(POWERTOGGLE)