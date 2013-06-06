import xbmc, xbmcgui, serial, binascii, sys, time

inNum = sys.argv[1]
inName = ""
sourceInNum = ''

if inNum == '1':
	sourceInNum = '\x81'
	inName = "WiDi"
elif inNum == '2':
	sourceInNum = '\x82'
	inName = "Apple TV 1"	
elif inNum == '3':
	sourceInNum = '\x83'
	inName = "ClickShare"
elif inNum == '4':
	sourceInNum = '\x84'
	inName = "Apple TV 2"		
elif inNum == '5':
	sourceInNum = '\x85'
	inName = "PC 1"		
elif inNum == '6':
	sourceInNum = '\x86'
	inName = "PC 2"		
elif inNum == '7':
	sourceInNum = '\x87'
	inName = "PC 3"		
elif inNum == '8':
	sourceInNum = '\x88'
	inName = "VADER"
else:
	inName = "Squirrel"
	print inNum
	
xbmc.executebuiltin('Notification(Video Source Control, Switching All Displays to ' + inName + ')')
serial.Serial(5, 9600, timeout=1).write('\x01' + sourceInNum + '\x81\x81')
time.sleep(0.1)
serial.Serial(5, 9600, timeout=1).write('\x01' + sourceInNum + '\x82\x81')
time.sleep(0.1)
serial.Serial(5, 9600, timeout=1).write('\x01' + sourceInNum + '\x83\x81')
