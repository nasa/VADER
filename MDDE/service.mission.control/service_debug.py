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
SWITCH_COM = 2
TUNER_COM = 12

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class DeviceStatus(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            print >>self.wfile, "<html><body>" + str(theCounter) + "<a href='/json'>Patient Test</a>" + str(theStatus) + "</body></html>"
        if 'json' in self.path:
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus))
        if 'tuner' in self.path:
            tunerParams = self.path.split('/')
            #print tunerParams
            theCommandQueue.append(tunerParams[1:])
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus['tuner']))
        if 'exec' in self.path:
            print >>self.wfile, '<html><body>command from executor'
            execParams = self.path.split('/')
            print >>self.wfile, execParams
            theCommandQueue.append(execParams[1:])
        if 'switch' in self.path:
            switchParams = self.path.split('/')
            #print switchParams
            theCommandQueue.append(switchParams[1:])
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus['outputs']))
        if 'display' in self.path:
            displayParams = self.path.split('/')
            #print displayParams
            theCommandQueue.append(displayParams[1:])
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus['outputs'][displayParams[2]]))

if (__name__ == "__main__"):
    xbmc.log('Version %s started' % __addonversion__)
    theCommandQueue = deque()
    theCounter = 0
    theInputs = {"1":{"name":"ClickShare","hexChar":'\x81'},"2":{"name":"MCC Video 1","hexChar":'\x82'},"3":{"name":"MCC Video 2","hexChar":'\x83'},"4":{"name":"MCC Video 3","hexChar":'\x84'},"5":{"name":"Apple TV","hexChar":'\x85'},"6":{"name":"WiDi","hexChar":'\x86'},"7":{"name":"VADER","hexChar":'\x87'},"8":{"name":"TV Tuner","hexChar":'\x88'},"0":{"name":"N/A","hexChar":'\x80'}}
    theOutputs = {"1":{"name":"Left","hexChar":'\x81',"comPort":"6"},"2":{"name":"Center A","hexChar":'\x82',"comPort":"9"},"3":{"name":"Center B","hexChar":'\x83',"comPort":"10"},"4":{"name":"Right A","hexChar":'\x84',"comPort":"8"},"5":{"name":"Right B","hexChar":'\x85',"comPort":"7"},"6":{"name":"Action Center","hexChar":'\x86',"comPort":"11"},"7":{"name":"HEVS 1","hexChar":'\x87',"comPort":"0"},"8":{"name":"HEVS 2","hexChar":'\x88',"comPort":"0"}}
    theStatus = {"outputs":[{"outputName":"Left","outputNumber":"1","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Center A","outputNumber":"2","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Center B","outputNumber":"3","inputNumber":"2","inputName":"MCC Video 1"},{"outputName":"Right A","outputNumber":"4","inputNumber":"1","inputName":"ClickShare"},{"outputName":"Right B","outputNumber":"5","inputNumber":"2","inputName":"MCC Video 1"},{"outputName":"Action Center","outputNumber":"6","inputNumber":"3","inputName":"MCC Video 2"},{"outputName":"HEVS 1","outputNumber":"7","inputNumber":"5","inputName":"Apple TV"},{"outputName":"HEVS 2","outputNumber":"8","inputNumber":"6","inputName":"WiDi"}],"tuner":{"majorChannel":"008","minorChannel":"001","channelName":"KUHT-HD","programName":"Daytripper"}}
    #theStatus = {'left': 1, 'center1': 1, 'center2': 2, 'right1': 1, 'right2':2, 'actionCenter': 3, 'HEVS1': 5, 'HEVS2': 6}
    httpd = ThreadedTCPServer(('', PORT), DeviceStatus)
    print "serving at port", PORT
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "starting the counter"
    while (not xbmc.abortRequested):
        time.sleep(0.1)
        theCounter += 1
        #print '*** Begin command section'
        while theCommandQueue:
            command = theCommandQueue.popleft()
            if command[0] == 'tuner':
                if command[1] == 'channel':
                    if command[2] == '+':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>P1\x0d')
                        ser.write('>TU\x0d')
                        ser.close()
                    elif command[2] == '-':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>P1\x0d')
                        ser.write('>TD\x0d')
                        ser.close()
                    else:
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>P1\x0d')
                        ser.write('>TC=' + command[2] + '\x0d')
                        ser.close()
                        print command[2]
                elif command[1] == 'power':
                    print command
                    if command[2] == 'on':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>P1\x0d')
                        ser.close()
                    elif command[2] == 'off':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>P0\x0d')
                        ser.close()
                    elif command[2] == 'toggle':
                        ser = serial.Serial(TUNER_COM, 9600, timeout=0.2)
                        ser.write('>PT\x0d')
                        ser.close()
            elif command[0] == 'exec':
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
                    xbmc.executebuiltin('Notification(Video Source Control, Resetting All Displays to Default')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x01\x82\x81\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x83\x82\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x84\x83\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x83\x84\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x82\x85\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x87\x86\x81')
                    ser.close()
                else:
                    xbmc.executebuiltin('Notification(Video Source Control, Switching ' + theOutputs[command[2]]["name"] + ' to ' + theInputs[command[1]]["name"] + ')')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x01' + theInputs[command[1]]["hexChar"] + theOutputs[command[2]]["hexChar"] + '\x81')
                    ser.close()
            elif command[0] == 'display':
                if command[2] == 'power':
                    # print theOutputs[command[1]]["comPort"]
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

        #print '*** End command section'
        time.sleep(0.1)
        
        # This is where the serial status stuff begins
        #print '*** Begin status section'
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x81\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][0]['inputNumber'] = source
            theStatus['outputs'][0]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 1'
            continue
        
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x82\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][1]['inputNumber'] = source
            theStatus['outputs'][1]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 2'
            continue
        
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x83\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][2]['inputNumber'] = source
            theStatus['outputs'][2]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 3'
            continue

        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x84\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][3]['inputNumber'] = source
            theStatus['outputs'][3]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 4'
            continue
        
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x85\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][4]['inputNumber'] = source
            theStatus['outputs'][4]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 5'
            continue
              
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x86\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][5]['inputNumber'] = source
            theStatus['outputs'][5]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 6'
            continue
              
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x87\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][6]['inputNumber'] = source
            theStatus['outputs'][6]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 7'
            continue
                
        try:
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x88\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            theStatus['outputs'][7]['inputNumber'] = source
            theStatus['outputs'][7]['inputName'] = theInputs[source]['name']
        except:
            print 'Exception in reading status of Switch Output 8'
            continue
            
        # Tuner read
        #print '* End Switch status and begin Tuner status'
        try:
            # print 'starting tuner read'
            ser = serial.Serial(TUNER_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('>ST\x0d')
            ser.read(4)
            majorChannel = ser.read(3)
            # print majorChannel
            ser.read(4)
            minorChannel = ser.read(3)
            # print minorChannel
            ser.close()
            theStatus['tuner']['majorChannel'] = majorChannel
            theStatus['tuner']['minorChannel'] = minorChannel
        except:
            print 'Exception in reading Tuner Channel Info'
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
            # print channelName
            ser.close()
            theStatus['tuner']['channelName'] = channelName
        except:
            print 'Exception in reading Tuner Channel Name'
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
            # print programName
            ser.close()
            theStatus['tuner']['programName'] = programName
        except:
            print 'Exception in reading Tuner Program Name'
            continue
        #print '*** End status section'
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"
