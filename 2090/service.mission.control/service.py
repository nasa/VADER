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
SWITCH_COM = 5

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
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus['outputs']))
        if 'display' in self.path:
            displayParams = self.path.split('/')
            #print displayParams
            theCommandQueue.append(displayParams[1:])
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", '*')
            self.end_headers()
            self.wfile.write(simplejson.dumps(theStatus['outputs'][int(displayParams[2])]))

if (__name__  == "__main__"):
    xbmc.log('Version %s started' % __addonversion__)
    theCommandQueue = deque()
    theCounter = 0
    theInputs = {"1":{"name":"WiDi","hexChar":'\x81'},"2":{"name":"ATV 1","hexChar":'\x82'},"3":{"name":"ClickShare","hexChar":'\x83'},"4":{"name":"ATV 2","hexChar":'\x84'},"5":{"name":"PC Input 1","hexChar":'\x85'},"6":{"name":"PC Input 2","hexChar":'\x86'},"7":{"name":"PC Input 3","hexChar":'\x87'},"8":{"name":"VADER","hexChar":'\x88'},"0":{"name":"N/A","hexChar":'\x80'}}
    theOutputs = {"1":{"name":"Left TV","hexChar":'\x81',"audioComPort":"7","videoComPort":"7"},"2":{"name":"Projector","hexChar":'\x82',"audioComPort":"6","videoComPort":"9"},"3":{"name":"Right TV","hexChar":'\x83',"audioComPort":"8","videoComPort":"8"},"5":{"name":"PC Monitor 1","hexChar":'\x85',"audioComPort":"0","videoComPort":"0"},"6":{"name":"PC Monitor 2","hexChar":'\x86',"audioComPort":"0","videoComPort":"0"},"7":{"name":"PC Monitor 3","hexChar":'\x87',"audioComPort":"0","videoComPort":"0"}}
    theStatus = {"outputs":[{"outputName":"Left TV","outputNumber":"1","inputNumber":"5","inputName":"ClickShare","powerStatus":"UNK","muteStatus":"UNK"},{"outputName":"Projector","outputNumber":"2","inputNumber":"1","inputName":"WiDi","powerStatus":"ON","muteStatus":"OFF"},{"outputName":"Right TV","outputNumber":"3","inputNumber":"8","inputName":"VADER","powerStatus":"UNK","muteStatus":"UNK"},{"outputName":"PC Monitor 1","outputNumber":"5","inputNumber":"5","inputName":"PC Input 1","powerStatus":"UNK","muteStatus":"UNK"},{"outputName":"PC Monitor 2","outputNumber":"6","inputNumber":"6","inputName":"PC Input 2","powerStatus":"UNK","muteStatus":"UNK"},{"outputName":"PC Monitor 3","outputNumber":"7","inputNumber":"7","inputName":"PC Input 3","powerStatus":"UNK","muteStatus":"UNK"}]}
    #theStatus = {'left': 1, 'center1': 1, 'center2': 2, 'right1': 1, 'right2':2, 'actionCenter': 3, 'HEVS1': 5, 'HEVS2': 6}
    httpd = ThreadedTCPServer(('', PORT), DeviceStatus)
    #print "serving at port", PORT
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    #print "starting the counter"
    while (not xbmc.abortRequested):
        time.sleep(0.1)
        theCounter += 1
        #print '*** Begin Command Section ' + str(theCounter)
        #print '**  Command Queue Size: ' + str(len(theCommandQueue))
        while theCommandQueue:
            #print '**  beginning of command queue loop'
            command = theCommandQueue.popleft()
            if command[0] == 'exec':
                #print'*   command type: SCRIPT EXECUTION'
                if len(command) == 1:
                    #print'    command: EXEC ERROR - NO SCRIPT SPECIFIED'
                    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Executor Error','No script specified for execution',5000,__icon__))
                elif len(command) == 2:
                    #print'    command: running ' + urllib.unquote_plus(command[1])
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ')')
                elif len(command) == 3:
                    #print'    command: running ' + urllib.unquote_plus(command[1])
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ',' + urllib.unquote_plus(command[2]) + ')')
                else:
                    #print'    command: running ' + urllib.unquote_plus(command[1])
                    xbmc.executebuiltin('RunScript(' + urllib.unquote_plus(command[1]) + ',' + urllib.unquote_plus(command[2]) + ',' + urllib.unquote_plus(command[3]) + ')')
            elif command[0] == 'switch':
                #print'*   device type: SWITCH'
                if command[1] == 'reset':
                    #print'    command type: RESET'
                    xbmc.executebuiltin('Notification(Video Source Control, Resetting All Displays to Default')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x01\x85\x81\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x86\x82\x81')
                    time.sleep(0.02)
                    ser.write('\x01\x87\x83\x81')
                    time.sleep(0.02)
                    ser.close()
                else:
                    #print'    command type: SET ' + theOutputs[command[2]]["name"] + ' TO ' + theInputs[command[1]]["name"]
                    xbmc.executebuiltin('Notification(Video Source Control, Switching ' + theOutputs[command[2]]["name"] + ' to ' + theInputs[command[1]]["name"] + ')')
                    ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
                    ser.write('\x01' + theInputs[command[1]]["hexChar"] + theOutputs[command[2]]["hexChar"] + '\x81')
                    ser.close()
            elif command[0] == 'display':
                #print'*   device type: DISPLAY'
                if command[1] == '2': #Projector/Receiver Hybrid
                    if command[2] == 'power':
                        #print'    command type: POWER TOGGLE ' + theOutputs[command[1]]["name"]
                        if theOutputs[command[1]]["powerStatus"] == 'ON':
                            ser = serial.Serial(int(theOutputs[command[1]]["videoComPort"]), 4800, timeout=0.3)
                            ser.write('\x3a\x50\x4f\x57\x52\x30\x0d')
                            ser.close()
                        else:
                            ser = serial.Serial(int(theOutputs[command[1]]["videoComPort"]), 4800, timeout=0.3)
                            ser.write('\x3a\x50\x4f\x57\x52\x31\x0d')
                            ser.close()
                    elif command[2] == 'volume':
                        #print'    command type: VOLUME ' + theOutputs[command[1]]["name"]
                        if command[3] == '+':
                            #print'    command: VOLUME UP'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x4d\x56\x55\x50\x0d')
                            ser.close()
                        elif command[3] == '-':
                            #print'    command: VOLUME DOWN'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x4d\x56\x44\x4f\x57\x4e\x0d')
                            ser.close()
                        elif command[3] == '0':
                            #print'    command: VOLUME ZERO'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x4d\x56\x39\x39\x0d')
                            ser.close()
                        else:
                            if command[4] == 'on':
                                #print'    command: MUTE ON'
                                ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                                ser.write('\x4d\x55\x4f\x4e\x0d')
                                ser.close()
                            elif command[4] == 'off':
                                #print'    command: MUTE OFF'
                                ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                                ser.write('\x4d\x55\x4f\x46\x46\x0d')
                                ser.close()
                            else:
                                #print'    command: MUTE TOGGLE'
                                ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                                if theOutputs[command[1]]["muteStatus"] == 'ON':
                                    ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                                    ser.write('\x4d\x55\x4f\x4e\x0d')
                                    ser.close()
                                else:
                                    ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                                    ser.write('\x4d\x55\x4f\x46\x46\x0d')
                                    ser.close()
                else:
                    if command[2] == 'power':
                        #print'    command type: POWER TOGGLE ' + theOutputs[command[1]]["name"]
                        ser = serial.Serial(int(theOutputs[command[1]]["videocomPort"]), 9600, timeout=0.3)
                        ser.write('\x08\x22\x00\x00\x00\x00\xd6')
                        ser.close()
                    elif command[2] == 'volume':
                        #print'    command type: VOLUME ' + theOutputs[command[1]]["name"]
                        if command[3] == '+':
                            #print'    command: VOLUME UP'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x08\x22\x01\x00\x01\x00\xd4')
                            ser.close()
                        elif command[3] == '-':
                            #print'    command: VOLUME DOWN'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x08\x22\x01\x00\x02\x00\xd3')
                            ser.close()
                        else:
                            #print'    command: MUTE'
                            ser = serial.Serial(int(theOutputs[command[1]]["audioComPort"]), 9600, timeout=0.3)
                            ser.write('\x08\x22\x02\x00\x00\x00\xd4')
                            ser.close()
            #print'**  ending of command queue loop'

        #print'*** End command section'
        time.sleep(0.1)
        
        # This is where the serial status stuff begins
        #print'*** Begin status section'
        try:
            #print'*   begin reading status of Switch Output 1'
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            #print'    serial port opened'
            ser.flushInput()
            #print'    serial input flushed'
            ser.write('\x05\x80\x81\x81')
            #print'    serial command written'
            ser.read(2)
            #print'    read 2 bytes to throw away'
            out = ser.read()
            #print'    read output byte'
            ser.close()
            #print'    closing serial port'
            foo = binascii.b2a_qp(out)
            #print'    converting binary to ascii'
            source = foo[2]
            #print'    putting results in status dictionary'
            theStatus['outputs'][0]['inputNumber'] = source
            theStatus['outputs'][0]['inputName'] = theInputs[source]['name']
            #print'*   finished reading status of Switch Output 1'
        except:
            print'Exception in reading status of Switch Output 1'
            continue
        
        try:
            #print'    begin reading status of Switch Output 2'
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
            #print'    finished reading status of Switch Output 2'
        except:
            print'Exception in reading status of Switch Output 2'
            continue
        
        try:
            #print'    begin reading status of Switch Output 3'
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
            #print'    finished reading status of Switch Output 3'
        except:
            print'Exception in reading status of Switch Output 3'
            continue

        try:
            #print '    begin reading status of Switch Output 4'
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            #print'    serial port opened' 
            ser.flushInput()
            #print'    serial input flushed'
            ser.write('\x05\x80\x84\x81')
            #print'    serial command written'
            ser.read(2)
            #print'    read 2 bytes to throw away'
            out = ser.read()
            #print'    read output byte'
            ser.close()
            #print'    closing serial port' 
            foo = binascii.b2a_qp(out)
            #print'    converting binary to ascii'
            source = foo[2]
            #theStatus['outputs'][3]['inputNumber'] = source
            #theStatus['outputs'][3]['inputName'] = theInputs[source]['name']
            #print '    finished reading status of Switch Output 4'
        except:
            print 'Exception in reading status of Switch Output 4'
            continue
        
        try:
            #print'    begin reading status of Switch Output 5'
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
            #print'    finished reading status of Switch Output 5'
        except:
            print 'Exception in reading status of Switch Output 5'
            continue
              
        try:
            #print'    begin reading status of Switch Output 6'
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
            #print'    finished reading status of Switch Output 6'
        except:
            print 'Exception in reading status of Switch Output 6'
            continue
              
        try:
            #print'    begin reading status of Switch Output 7'
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
            #print'    finished reading status of Switch Output 7'
        except:
            print 'Exception in reading status of Switch Output 7'
            continue
                
        try:
            #print'    begin reading status of Switch Output 8'
            ser = serial.Serial(SWITCH_COM, 9600, timeout=0.3)
            ser.flushInput()
            ser.write('\x05\x80\x88\x81')
            ser.read(2)
            out = ser.read()
            ser.close()
            foo = binascii.b2a_qp(out)
            source = foo[2]
            #theStatus['outputs'][7]['inputNumber'] = source
            #theStatus['outputs'][7]['inputName'] = theInputs[source]['name']
            #print'    finished reading status of Switch Output 8'
        except:
            print'Exception in reading status of Switch Output 8'
            continue
            
        # Tuner read
        print '**  End Switch status and begin Projector/Receiver status'
        try:
            print '    starting projector power status read'
            ser = serial.Serial(int(theOutputs["2"]["videoComPort"]), 4800, timeout=0.3)
            ser.flushInput()
            ser.write('\x3a\x50\x4f\x53\x54\x3f\x0d')
            ser.read(15)
            powerStatus = ser.read()
            print '    ' + powerStatus
            ser.flushInput()
            ser.close()
            if muteStatus == '3':
                theStatus['outputs'][1]['powerStatus'] = 'ON'
            else:
                theStatus['outputs'][1]['powerStatus'] = 'OFF'
            print '    finished projector power status read'
        except:
            print 'Exception in reading projector power status'
            continue

        try:
            print '    starting receiver mute status read'
            ser = serial.Serial(int(theOutputs["2"]["audioComPort"]), 9600, timeout=0.3)
            ser.flushInput()
            ser.write('MU?\x0d')
            ser.read(2)
            muteStatus = ser.read()
            print '    ' + muteStatus
            ser.flushInput()
            ser.close()
            if muteStatus == 'O':
                theStatus['outputs'][1]['muteStatus'] = 'ON'
            else:
                theStatus['outputs'][1]['muteStatus'] = 'OFF'
            print '    finished receiver mute status read'
        except:
            print 'Exception in reading receiver mute status'
            continue
        
        # print '*** End status section'
    print "starting server shutdown"
    httpd.shutdown()
    print "finished server shutdown"