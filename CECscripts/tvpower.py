import sys, subprocess, string, xbmc, xbmcgui

class MyClass(xbmcgui.Window):
	def __init__(self):
                xbmc.executebuiltin("Notification(Shutdown, Powering off TV...)")
                output = subprocess.check_output('echo "pow 0" | cec-client -d 1 -s | tail -n1 | grep "power"', shell=True)

                if string.find(output, "on") > -1:
                        subprocess.call("echo 'standby 0' | cec-client -s", shell=True)
                else:
                        subprocess.call("echo 'on 0' | cec-client -s", shell=True)

myTestScript = MyClass()
del myTestScript
