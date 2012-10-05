import sys, xbmc, xbmcgui, subprocess, time

class MyClass(xbmcgui.Window):
	def __init__(self):
		subprocess.call("echo 'as' | cec-client -p 1 -s", shell=True)

myTestScript = MyClass()
del myTestScript
