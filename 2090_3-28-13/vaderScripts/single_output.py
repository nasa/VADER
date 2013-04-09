import xbmc, xbmcgui, serial, binascii, sys, time

inNum = sys.argv[1]
outNum = sys.argv[2]

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

if outNum == '1':
	sourceOutNum = '\x81'
	outName = "Left TV"
elif outNum == '2':
	sourceOutNum = '\x82'
	outName = "Projector"
elif outNum == '3':
	sourceOutNum = '\x83'	
	outName = "Right TV"

xbmc.executebuiltin('Notification(Video Source Control, Switching ' + outName + ' to ' + inName + ')')
print inNum
serial.Serial(5, 9600, timeout=1).write('\x01' + sourceInNum + sourceOutNum + '\x81')
