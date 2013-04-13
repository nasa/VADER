import re
import os
import sys
import time
import SocketServer
import SimpleHTTPServer
from threading import Thread
from collections import deque
import xbmc
import xbmcaddon
import xbmcgui
import binascii

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

class DeviceStatus(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            print >>self.wfile, "<html><body>" + str(theCounter) + "<a href='/run'>Patient Test</a>" + str(theStatus) + "</body></html>"
        if self.path == '/run':
            print 'Patience is a virtue...'
            print >>self.wfile, "<html><body>" + str(theCounter) + "<a href='/'>Impatient Test</a>" + str(theStatus) + "</body></html>"
        if 'tuner' in self.path:
            print >>self.wfile, '<html><body>command for tuner'
            tunerParams = self.path.split('/')
            print >>self.wfile, tunerParams
            theCommandQueue.append(tunerParams[1:])
        if 'executor' in self.path:
            print >>self.wfile, '<html><body>command from executor'
            execParams = self.path.split('/')
            print >>self.wfile, execParams
            theCommandQueue.append(execParams[1:])

def startServing(server):
    print "begin serving requests"
    server.serve_forever()

if (__name__ == "__main__"):
    xbmc.log('Version %s started' % __addonversion__)
    theCommandQueue = deque()
    theCounter = 0
    theStatus = {'left': 1, 'center1': 1, 'center2': 2, 'right1': 1, 'right2':2, 'actionCenter': 3, 'HEVS1': 4, 'HEVS2': 5}
    httpd = SocketServer.TCPServer(('', PORT), DeviceStatus)
    print "serving at port", PORT
    Thread(target=startServing, args=(httpd,)).start()
    print "starting the counter"
    while (not xbmc.abortRequested):
        time.sleep(1)
        theCounter += 1
        while theCommandQueue:
            command = theCommandQueue.popleft()
            if command[0] == 'tuner':
                if command[1] == 'channel':
                    if command[2] == '+':
                        serial.Serial(3, 9600, timeout=1).write('>P1\x0d')
                        #serial.Serial(3, 9600, timeout=1).write('\x3e\x54\x55\x0d')
                        serial.Serial(3, 9600, timeout=1).write('>TU\x0d')
                    elif command[2] == '-':
                        serial.Serial(3, 9600, timeout=1).write('>P1\x0d')
                        serial.Serial(3, 9600, timeout=1).write('>TD\x0d')
                    else:
                        serial.Serial(3, 9600, timeout=1).write('>P1\x0d')
                        serial.Serial(3, 9600, timeout=1).write('>TC=' + command[2] + '\x0d')
                        print command[2]
                elif command[1] == 'power':
                    print command
                    if command[2] == 'on':
                        serial.Serial(3, 9600, timeout=1).write('>P1\x0d')
                    elif command[2] == 'off':
                        serial.Serial(3, 9600, timeout=1).write('>P0\x0d')
                    elif command[2] == 'toggle':
                        serial.Serial(3, 9600, timeout=1).write('>PT\x0d')
            elif command[0] == 'exec':
                pass

        #serial.Serial(3, 9600, timeout=1).write('\x3e\x50\x31\x0d')
        
        # This is where the serial stuff begins
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x81\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['left'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x82\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['center1'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x83\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['center2'] = source
        except:
            continue

        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x84\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['right1'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x85\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['right2'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x86\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['actionCenter'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x87\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['HEVS1'] = source
        except:
            continue
        
        try:
            ser = serial.Serial(2, 9600, timeout=1)
            ser.flushInput()
            ser.write('\x05\x80\x88\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['HEVS2'] = source
        except:
            continue
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"
