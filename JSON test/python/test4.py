import xbmc, xbmcgui, sys, time

inName1 = sys.argv[1]
inName2 = sys.argv[2]

xbmc.executebuiltin('Notification(Kaiju Attack, ' + inName1 + ' and ' + inName2 + ' are coming!)')