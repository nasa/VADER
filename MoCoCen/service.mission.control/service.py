import re
import os
import sys
import time
import binascii
import urllib
import SocketServer
import SimpleHTTPServer
import threading
from collections import deque
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
SWITCH_COM = 6
DISPLAY_COM = 7

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class DeviceStatus(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            print >>self.wfile, "<html><body>" + str(theCounter) + "<a href='/json'>Patient Test</a>" + str(theStatus) + "</body></html>"
        if self.path == '/counter':
            print >>self.wfile, "<html><body>" + str(theCounter) + "</body></html>"
        if 'json' in self.path:
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus))
        if 'exec' in self.path:
            print >>self.wfile, '<html><body>command from executor'
            execParams = self.path.split('/')
            print >>self.wfile, execParams
            theCommandQueue.append(execParams[1:])
        if 'switch' in self.path:
            print >>self.wfile, '<html><body>command for switch'
            switchParams = self.path.split('/')
            print >>self.wfile, switchParams
            theCommandQueue.append(switchParams[1:])
        if 'display' in self.path:
            print >>self.wfile, '<html><body>command for display'
            displayParams = self.path.split('/')
            print >>self.wfile, displayParams
            theCommandQueue.append(displayParams[1:])

if (__name__ == "__main__"):
    xbmc.log('Version %s started' % __addonversion__)
    theCommandQueue = deque()
    theCounter = 0
    theInputs = {"1":{"name":"VADER","hexChar":'\x01\xa5'},"2":{"name":"WiDi","hexChar":'\x02\x47'},"3":{"name":"Wireless HDMI","hexChar":'\x03\x19'},"4":{"name":"Apple TV","hexChar":'\x04\x9a'},"5":{"name":"ClickShare","hexChar":'\x05\xc4'},"6":{"name":"Multi-Display","hexChar":'\x06\x26'},"7":{"name":"Table Input","hexChar":'\x07\x78'},"8":{"name":"Input8","hexChar":'\x08\x39'},"0":{"name":"N/A","hexChar":'\x00'}}
    theOutputs = {"1":{"name":"TV","hexChar":'\x00',"comPort":DISPLAY_COM}}
    theStatus = {"outputs":[{"outputName":"TV","outputNumber":"1","inputNumber":"1","inputName":"VADER"}]}
    #theStatus = {'left': 1, 'center1': 1, 'center2': 2, 'right1': 1, 'right2':2, 'actionCenter': 3, 'HEVS1': 5, 'HEVS2': 6}
    httpd = ThreadedTCPServer(('', PORT), DeviceStatus)
    print "serving at port", PORT
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "starting the counter"
    while (not xbmc.abortRequested):
        theCounter += 1
        while theCommandQueue:
            command = theCommandQueue.popleft()
            if command[0] == 'exec':
                if len(command) == 1:
                    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Executor Error','No script specified for execution',5000,__icon__))
                elif len(command) == 2:
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ')')
                elif len(command) == 3:
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ',' + urllib.unquote_plus(command[2]) + ')')
                else:
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ',' + urllib.unquote_plus(command[2]) + ',' + urllib.unquote_plus(command[3]) + ')')
            elif command[0] == 'switch':
                if command[1] == 'reset':
                    xbmc.executebuiltin('Notification(Video Source Control, Resetting Display to Default')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x20\x02\x01\x01\xa5')
                    time.sleep(0.02)
                    ser.close()
                else:
                    xbmc.executebuiltin('Notification(Video Source Control, Switching ' + theOutputs[command[2]]["name"] + ' to ' + theInputs[command[1]]["name"] + ')')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x20\x02\x01' + theInputs[command[1]]["hexChar"])
                    ser.close()
            elif command[0] == 'display':
                if command[2] == 'power':
                    if len(command) == 4:
						if command[3] == 'on':
							ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
							ser.write('\x08\x22\x00\x00\x00\x02\xd4')
							ser.close()
						elif command[3] == 'off':
							ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
							ser.write('\x08\x22\x00\x00\x00\x01\xd5')
							ser.close()
                    else:
                        ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
                        ser.write('\x08\x22\x00\x00\x00\x00\xd6')
                        ser.close()
                elif command[2] == 'volume':
                    if command[3] == '+':
                        ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
                        ser.write('\x08\x22\x01\x00\x01\x00\xd4')
                        ser.close()
                    elif command[3] == '-':
                        ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
                        ser.write('\x08\x22\x01\x00\x02\x00\xd3')
                        ser.close()
                    else:
                        ser = serial.Serial(int(theOutputs[command[1]]["comPort"]), 9600, timeout=0.3)
                        ser.write('\x08\x22\x02\x00\x00\x00\xd4')
                        ser.close()

        time.sleep(0.1)
        
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"