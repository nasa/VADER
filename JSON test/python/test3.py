import xbmc, xbmcgui, sys, time

inName = sys.argv[1]

xbmc.executebuiltin('Notification(Kaiju Attack, ' + inName + ' is coming!)')