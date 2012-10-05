import sys, xbmc, xbmcgui, subprocess

class MyClass(xbmcgui.Window):
	def __init__(self):
		subprocess.call("echo 'as' | cec-client -p 3 -s", shell=True)

myTestScript = MyClass()
del myTestScript
