import sys, xbmc, xbmcgui, subprocess

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_BACKSPACE = 110

class MyClass(xbmcgui.Window):
	def __init__(self):
           subprocess.call("echo 'as' | cec-client -p 2 -s", shell=True)

	def onAction(self, action):
           print action
           if action == ACTION_PREVIOUS_MENU:
                subprocess.call("echo 'as' | cec-client -p 1 -s", shell=True)
                self.close()
           elif action == ACTION_NAV_BACK:
                subprocess.call("echo 'as' | cec-client -p 1 -s", shell=True)
                self.close()
           elif action == ACTION_BACKSPACE:
                subprocess.call("echo 'as' | cec-client -p 1 -s", shell=True)
                self.close()

myTestScript = MyClass()
myTestScript .doModal()
del myTestScript
