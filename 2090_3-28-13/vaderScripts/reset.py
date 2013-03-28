import xbmc, xbmcgui, serial, binascii, sys, time

	
xbmc.executebuiltin('Notification(Video Source Control, Resetting All Displays to Default')
serial.Serial(5, 9600, timeout=1).write('\x01\x85\x81\x81')
time.sleep(0.1)
serial.Serial(5, 9600, timeout=1).write('\x01\x86\x82\x81')
time.sleep(0.1)
serial.Serial(5, 9600, timeout=1).write('\x01\x87\x83\x81')
