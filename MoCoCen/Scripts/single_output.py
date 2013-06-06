import xbmc, xbmcgui, binascii, sys, time, serial

inNum = sys.argv[1]

print "test"
	
if inNum == '1':
	inName="VADER"
	#xbmc.executebuiltin("RunScript(C:\vaderScripts\switch-vader.py)")
	#xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\switch-vader.py)')
	xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\mococenSerial\\serial-switchVADER.py)')
elif inNum == '2':
	inName="WiDi"
	#xbmc.RunScript(RunScript("C:\vaderScripts\switch-widi.py"))
	#xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\switch-widi.py)')
	xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\mococenSerial\\serial-switchWIDI.py)')
elif inNum == '3':
	inName="Wireless HDMI"
	#xbmc.RunScript("C:\vaderScripts\switch-wirelessHDMI.py")
	#xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\switch-wirelessHDMI.py)')
	xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\mococenSerial\\serial-switchWIHDMI.py)')
elif inNum == '4':
	inName="Apple TV"
	#xbmc.executebuiltin("RunScript(C:\\vaderScripts\switch-atv.py)")
	#xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\switch-atv.py)')
	xbmc.executebuiltin('XBMC.RunScript(C:\\vaderScripts\\mococenSerial\\serial-switchATV.py)')
else:
	inName="Input Error"
	

xbmc.executebuiltin('Notification(Video Source Control, Switching ' + inNum + ' to ' + inName + ')')