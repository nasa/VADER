import re
import os
import sys
import time
import SocketServer
import SimpleHTTPServer
from threading import Thread
import xbmc
import xbmcaddon
import xbmcgui

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__        = xbmcaddon.Addon(id='service.mission.control')
__addonid__      = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__addonname__    = __addon__.getAddonInfo('name')
__author__       = __addon__.getAddonInfo('author')
__icon__         = __addon__.getAddonInfo('icon')
__cwd__          = __addon__.getAddonInfo('path').decode("utf-8")
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

import serial

PORT = 8000

class SwitchStatus(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            print >>self.wfile, "<html><body><a href='/run'>Patient Test</a>" + str(theCounter) + "</body></html>"
        if self.path == '/run':
            print 'Patience is a virtue...'
            print >>self.wfile, "<html><body><a href='/'>Impatient Test</a>" + str(theCounter) + "</body></html>"

def startServing(server):
    print "begin serving requests"
    server.serve_forever()

if (__name__ == "__main__"):
    xbmc.log('Version %s started' % __addonversion__)
    theCounter = 0
    httpd = SocketServer.TCPServer(('', PORT), SwitchStatus)
    print "serving at port", PORT
    Thread(target=startServing, args=(httpd,)).start()
    print "starting the counter"
    while (not xbmc.abortRequested):
        time.sleep(2.5)
        theCounter += 1
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"