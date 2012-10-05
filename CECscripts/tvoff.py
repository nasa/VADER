import sys, xbmc, xbmcgui, subprocess

class MyClass(xbmcgui.Window):
	def __init__(self):
		subprocess.call("echo 'standby 0' | cec-client -s", shell=True)

myTestScript = MyClass()
del myTestScript
