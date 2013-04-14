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
SWITCH_COM = 2
TUNER_COM = 2

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
    theStatus = {"outputs":[{"outputName":"Left","outputNumber":"1","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Center A","outputNumber":"2","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Center B","outputNumber":"3","inputNumber":"2","inputName":"MCC Video 1"},{"outputName":"Right A","outputNumber":"4","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Right B","outputNumber":"5","inputNumber":"2","inputName":"MCC Video 1"},{"outputName":"Action Center","outputNumber":"6","inputNumber":"3","inputName":"MCC Video 2"},{"outputName":"HEVS 1","outputNumber":"7","inputNumber":"5","inputName":"Apple TV"},{"outputName":"HEVS 2","outputNumber":"8","inputNumber":"6","inputName":"WiDi"}],"tuner":{"majorChannel":"008","minorChannel":"001","channelName":"KUHT-HD","programName":"Daytripper"}}
    #theStatus = {'left': 1, 'center1': 1, 'center2': 2, 'right1': 1, 'right2':2, 'actionCenter': 3, 'HEVS1': 5, 'HEVS2': 6}
    httpd = SocketServer.TCPServer(('', PORT), DeviceStatus)
    print "serving at port", PORT
    Thread(target=startServing, args=(httpd,)).start()
    print "starting the counter"
    while (not xbmc.abortRequested):
        time.sleep(0.5)
        theCounter += 1
        while theCommandQueue:
            command = theCommandQueue.popleft()
            if command[0] == 'tuner':
                if command[1] == 'channel':
                    if command[2] == '+':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
                        ser.write('>P1\x0d')
                        ser.write('>TU\x0d')
                        ser.close()
                    elif command[2] == '-':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
                        ser.write('>P1\x0d')
                        ser.write('>TD\x0d')
                        ser.close()
                    else:
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
                        ser.write('>P1\x0d')
                        ser.write('>TC=' + command[2] + '\x0d')
                        ser.close()
                        print command[2]
                elif command[1] == 'power':
                    print command
                    if command[2] == 'on':
                        serial.Serial(TUNER_COM, 9600, timeout=1).write('>P1\x0d')
                    elif command[2] == 'off':
                        serial.Serial(TUNER_COM, 9600, timeout=1).write('>P0\x0d')
                    elif command[2] == 'toggle':
                        serial.Serial(TUNER_COM, 9600, timeout=1).write('>PT\x0d')
            elif command[0] == 'exec':
                pass

        time.sleep(0.5)
        
        # This is where the serial status stuff begins
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x81\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][0]['inputNumber'] = source
            # #theStatus['left'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x82\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][1]['inputNumber'] = source
            # #theStatus['center1'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x83\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][2]['inputNumber'] = source
            # #theStatus['center2'] = source
        # except:
            # continue

        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x84\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][3]['inputNumber'] = source
            # #theStatus['right1'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x85\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][4]['inputNumber'] = source
            # #theStatus['right2'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x86\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][5]['inputNumber'] = source
            # #theStatus['actionCenter'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x87\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][6]['inputNumber'] = source
            # #theStatus['HEVS1'] = source
        # except:
            # continue
        
        # try:
            # ser = serial.Serial(2, 9600, timeout=1)
            # ser.flushInput()
            # ser.write('\x05\x80\x88\x81')
            # ser.read(2)
            # out = ser.read()
            # ser.close()
            # foo = binascii.b2a_qp(out)
            # source = foo[2]
            # theStatus['outputs'][7]['inputNumber'] = source
            # #theStatus['HEVS2'] = source
        # except:
            # continue
        
        # Tuner read
        try:
            #print 'starting tuner read'
            ser = serial.Serial(TUNER_COM, 9600, timeout=0.5)
            ser.flushInput()
            ser.write('>ST\x0d')
            ser.read(4)
            majorChannel = ser.read(3)
            #print majorChannel
            ser.read(4)
            minorChannel = ser.read(3)
            #print minorChannel
            ser.close()
            theStatus['tuner']['majorChannel'] = majorChannel
            theStatus['tuner']['minorChannel'] = minorChannel
        except:
            continue
        
        try:
            ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('>NC\x0d')
            ser.read(4)
            channelName = ''
            while True:
                byte=ser.read()
                if byte == '\r':
                    break
                channelName += byte
            #print channelName
            ser.close()
            theStatus['tuner']['channelName'] = channelName
        except:
            continue
        
        try:
            ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('>NP\x0d')
            ser.read(4)
            programName = ''
            while True:
                byte=ser.read()
                if byte == '\r':
                    break
                programName += byte
            #print programName
            ser.close()
            theStatus['tuner']['programName'] = programName
        except:
            continue
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"
