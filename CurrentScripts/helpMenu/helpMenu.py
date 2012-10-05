import xbmc, xbmcgui
 
#get actioncodes from keymap.xml
ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_BACKSPACE = 110
 
class MainClass(xbmcgui.WindowDialog):
	def __init__(self):
		self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))	
		# Top Menu Text
		self.strActionInfo = xbmcgui.ControlLabel(570, 60, 200, 200, 'Help Menu', 'Font_Bold35', '0xFF000000')
		self.addControl(self.strActionInfo)

		self.strActionInfo = xbmcgui.ControlLabel(550, 100, 300, 200, 'Select a Topic', 'Font_Bold35', '0xFF000000')
		self.addControl(self.strActionInfo)

		#Location & size of source buttons 
	
		self.gettingStartedButton = xbmcgui.ControlButton(300, 150, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/gettingStartedIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTgettingStartedIcon.jpg')
		self.addControl(self.gettingStartedButton)	
	
		self.iptvButton = xbmcgui.ControlButton(300, 275, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/iptvIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTiptvIcon.jpg')
		self.addControl(self.iptvButton)
		
		self.imagesButton = xbmcgui.ControlButton(300, 400, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/imagesIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTimagesIcon.jpg')
		self.addControl(self.imagesButton)

		self.videosButton = xbmcgui.ControlButton(300, 525, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/videosIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTvideosIcon.jpg')
		self.addControl(self.videosButton)
		
		self.remoteButton = xbmcgui.ControlButton(650, 150, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/remoteIcon2.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTremoteIcon2.jpg')
		self.addControl(self.remoteButton)		
	
		self.sourceButton = xbmcgui.ControlButton(650, 275, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/sourceIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTsourceIcon.jpg')
		self.addControl(self.sourceButton)		

		self.documentsButton = xbmcgui.ControlButton(650, 400, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/documentsIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTdocumentsIcon.jpg')
		self.addControl(self.documentsButton)		
		
		self.webControlButton = xbmcgui.ControlButton(650, 525, 350, 125, '', textOffsetY=20, textColor='0xFF000000', focusedColor='0xFF000000', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/webIcon.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/MainMenuIcons/FTwebIcon.jpg')
		self.addControl(self.webControlButton)			
		
		#Start flashing icon on Projector Icon
		self.setFocus(self.gettingStartedButton)
		
		#Moves buttons can make
		self.gettingStartedButton.controlLeft(self.remoteButton)
		self.gettingStartedButton.controlRight(self.remoteButton)
		self.gettingStartedButton.controlUp(self.videosButton)
		self.gettingStartedButton.controlDown(self.iptvButton)
		
		self.iptvButton.controlLeft(self.sourceButton)
		self.iptvButton.controlRight(self.sourceButton)
		self.iptvButton.controlUp(self.gettingStartedButton)
		self.iptvButton.controlDown(self.imagesButton)	
		
		self.imagesButton.controlLeft(self.documentsButton)
		self.imagesButton.controlRight(self.documentsButton)
		self.imagesButton.controlUp(self.iptvButton)
		self.imagesButton.controlDown(self.videosButton)	

		self.videosButton.controlLeft(self.webControlButton)
		self.videosButton.controlRight(self.webControlButton)
		self.videosButton.controlUp(self.imagesButton)
		self.videosButton.controlDown(self.gettingStartedButton)	

		self.remoteButton.controlLeft(self.gettingStartedButton)
		self.remoteButton.controlRight(self.gettingStartedButton)		
		self.remoteButton.controlUp(self.webControlButton)		
		self.remoteButton.controlDown(self.sourceButton)			

		self.sourceButton.controlLeft(self.iptvButton)
		self.sourceButton.controlRight(self.iptvButton)
		self.sourceButton.controlUp(self.remoteButton)
		self.sourceButton.controlDown(self.documentsButton)	

		self.documentsButton.controlLeft(self.imagesButton)
		self.documentsButton.controlRight(self.imagesButton)
		self.documentsButton.controlUp(self.sourceButton)
		self.documentsButton.controlDown(self.webControlButton)			

		self.webControlButton.controlLeft(self.videosButton)
		self.webControlButton.controlRight(self.videosButton)
		self.webControlButton.controlUp(self.documentsButton)
		self.webControlButton.controlDown(self.remoteButton)			
	
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()
		elif action == ACTION_BACKSPACE:
			self.close()	
	#Button paths to child pages
	def onControl(self, control):
		if control == self.remoteButton:
			popup = remotePage()
			popup .doModal()
			del popup
		elif control == self.iptvButton:
			self.setFocus(self.iptvButton)		
			popup = iptvPage()
			popup .doModal()
			del popup
		elif control == self.imagesButton:	
			self.setFocus(self.imagesButton)			
			popup = imagesPage()
			popup .doModal()
			del popup	
		elif control == self.videosButton:	
			self.setFocus(self.videosButton)			
			popup = videosPage()
			popup .doModal()
			del popup	
		elif control == self.documentsButton:	
			self.setFocus(self.documentsButton)		
			popup = documentsPage()
			popup .doModal()
			del popup	
		elif control == self.sourceButton:	
			self.setFocus(self.sourceButton)				
			popup = sourcePage()
			popup .doModal()
			del popup	
		elif control == self.gettingStartedButton:
			self.setFocus(self.gettingStartedButton)	
			self.close()		
			popup = gettingStartedPage()
			popup .doModal()
			del popup	
		elif control == self.webControlButton:	
			self.setFocus(self.webControlButton)			
			popup = webControlPage()
			popup .doModal()
			del popup				

#Child Pages			
class remotePage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(570, 60, 200, 200, 'Front View', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)
	
	#3 buttons: Image, left and right arrow
    self.remoteImage1 = xbmcgui.ControlButton(395, 105, 537, 527, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/remoteKeysFront.jpg')
    self.addControl(self.remoteImage1)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.rightArrow = xbmcgui.ControlButton(650, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/rightArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTrightArrow.jpg')
    self.addControl(self.rightArrow)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.rightArrow)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.rightArrow)
    self.leftArrow.controlRight(self.rightArrow)		

    self.rightArrow.controlLeft(self.leftArrow)
    self.rightArrow.controlRight(self.leftArrow)			

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()		
			
  #Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.rightArrow:	
  		popup = remotePage2()
  		popup .doModal()
  		del popup	
        self.close()
			
class remotePage2(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(570, 60, 200, 200, 'Back View', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image, left and homeButton
    self.remoteImage2 = xbmcgui.ControlButton(280, 200, 750, 365, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/keyboardKeys.jpg')
    self.addControl(self.remoteImage2)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.homeButton = xbmcgui.ControlButton(650, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.homeButton)
    self.leftArrow.controlRight(self.homeButton)

    self.homeButton.controlLeft(self.leftArrow)
    self.homeButton.controlRight(self.leftArrow)	

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.homeButton:	
  		self.close()

class iptvPage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(610, 60, 200, 200, 'IPTV', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image,  homeButton
    self.iptvImage = xbmcgui.ControlButton(280, 130, 750, 418,  '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/iptvHelp.jpg')
    self.addControl(self.iptvImage)		

    self.homeButton = xbmcgui.ControlButton(600, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.homeButton:	
  		self.close()

class imagesPage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(590, 60, 200, 200, 'Images', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image, left and right arrow
    self.imagesImage1 = xbmcgui.ControlButton(280, 130, 750, 420, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/imagesHelp.jpg')
    self.addControl(self.imagesImage1)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.rightArrow = xbmcgui.ControlButton(650, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/rightArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTrightArrow.jpg')
    self.addControl(self.rightArrow)
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.rightArrow)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.rightArrow)
    self.leftArrow.controlRight(self.rightArrow)		

    self.rightArrow.controlLeft(self.leftArrow)
    self.rightArrow.controlRight(self.leftArrow)			

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.rightArrow:	
  		popup = imagesPage2()
  		popup .doModal()
  		del popup	
        self.close()
        
class imagesPage2(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(555, 60, 300, 200, 'Images (cont)', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image, left and right arrow
    self.imagesImage2 = xbmcgui.ControlButton(280, 130, 750, 422, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/imagesHelp2.jpg')
    self.addControl(self.imagesImage2)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.rightArrow = xbmcgui.ControlButton(650, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/rightArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTrightArrow.jpg')
    self.addControl(self.rightArrow)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.rightArrow)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.rightArrow)
    self.leftArrow.controlRight(self.rightArrow)		

    self.rightArrow.controlLeft(self.leftArrow)
    self.rightArrow.controlRight(self.leftArrow)			

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.rightArrow:	
  		popup = imagesPage3()
  		popup .doModal()
  		del popup	
        self.close()  		

class imagesPage3(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(555, 60, 300, 200, 'Images (cont)', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image, left and homeButton
    self.imagesImage3 = xbmcgui.ControlButton(310, 110, 706, 500, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/imagesHelp3.jpg')
    self.addControl(self.imagesImage3)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.homeButton = xbmcgui.ControlButton(650, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)		
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.homeButton)
    self.leftArrow.controlRight(self.homeButton)

    self.homeButton.controlLeft(self.leftArrow)
    self.homeButton.controlRight(self.leftArrow)	

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.homeButton:	
  		self.close()

class videosPage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(610, 60, 200, 200, 'Videos', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image,  homeButton
    self.videosImage = xbmcgui.ControlButton(280, 110, 748, 481, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/videosHelp.jpg')
    self.addControl(self.videosImage)		

    self.homeButton = xbmcgui.ControlButton(600, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.homeButton:	
  		self.close()

class documentsPage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(570, 60, 200, 200, 'Documents', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image,  homeButton
    self.documentsImage = xbmcgui.ControlButton(280, 130, 750, 400, 'image')
    self.addControl(self.documentsImage)		

    self.homeButton = xbmcgui.ControlButton(600, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.homeButton:	
  		self.close()

class sourcePage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(515, 60, 400, 200, 'A/V Source Control', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)
	#3 buttons: Image, left and right arrow
    self.sourceImage1 = xbmcgui.ControlButton(280, 130, 750, 474, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/sourceHelp.jpg')
    self.addControl(self.sourceImage1)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.rightArrow = xbmcgui.ControlButton(650, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/rightArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTrightArrow.jpg')
    self.addControl(self.rightArrow)
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.rightArrow)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.rightArrow)
    self.leftArrow.controlRight(self.rightArrow)		

    self.rightArrow.controlLeft(self.leftArrow)
    self.rightArrow.controlRight(self.leftArrow)			

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()		
			
  #Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.rightArrow:	
  		popup = sourcePage2()
  		popup .doModal()
  		del popup	
        self.close()  		
			
class sourcePage2(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(465, 60, 500, 200, 'A/V Source Control (cont)', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)

	#3 buttons: Image, left and homeButton
    self.sourceImage2 = xbmcgui.ControlButton(280, 110, 746, 483, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/sourceHelp2.jpg')
    self.addControl(self.sourceImage2)		
	
    self.leftArrow = xbmcgui.ControlButton(550, 600, 100, 80, '', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/leftArrow.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FTleftArrow.jpg')
    self.addControl(self.leftArrow)

    self.homeButton = xbmcgui.ControlButton(650, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)		
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
    #Moves buttons can make
    self.leftArrow.controlLeft(self.homeButton)
    self.leftArrow.controlRight(self.homeButton)

    self.homeButton.controlLeft(self.leftArrow)
    self.homeButton.controlRight(self.leftArrow)	

  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.leftArrow:
  		self.close()
  	elif control == self.homeButton:	
  		self.close()
			
class gettingStartedPage(xbmcgui.WindowDialog):
  def __init__(self):
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )        
    playlist.clear()        
    playlist.add('/home/vader/videos/curiosity.mp4')        
    xbmc.Player().play( playlist)  
	  
    self.homeButton = xbmcgui.ControlButton(600, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.homeButton:	
		xbmc.Player().stop()    	
 		popup = MainClass()
		popup .doModal()
		del popup   
 		self.close() 
    
  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			xbmc.Player().stop()  
			self.close()
		elif action == ACTION_NAV_BACK:
			xbmc.Player().stop()  		
			self.close()			
		elif action == ACTION_BACKSPACE:
			xbmc.Player().stop()  		
			self.close()			

class webControlPage(xbmcgui.WindowDialog):
  def __init__(self):
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, '/home/vader/.xbmc/scripts/helpMenu/helpMenuBackground.jpg'))
    self.strActionInfo = xbmcgui.ControlLabel(570, 60, 200, 200, 'Web Control', 'Font_Bold35', '0xFF000000')
    self.addControl(self.strActionInfo)


	#3 buttons: Image,  homeButton
    self.extraImage = xbmcgui.ControlButton(280, 130, 750, 400, 'image')
    self.addControl(self.extraImage)		

    self.homeButton = xbmcgui.ControlButton(600, 600, 100, 80, 'Home', font='Font_Bold24', noFocusTexture='/home/vader/.xbmc/scripts/helpMenu/homeButton.jpg', focusTexture='/home/vader/.xbmc/scripts/helpMenu/FThomeButton.jpg', textOffsetY=25, textOffsetX=18, textColor='0xFFFFFFFF', focusedColor='0xFFD9D919')
    self.addControl(self.homeButton)	
    
    #Start flashing icon on Projector Icon
    self.setFocus(self.homeButton)
    
  def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		elif action == ACTION_NAV_BACK:
			self.close()			
		elif action == ACTION_BACKSPACE:
			self.close()			

	#Button paths to child pages
  def onControl(self, control):
  	if control == self.homeButton:	
  		self.close()

mydisplay = MainClass()
mydisplay .doModal()
del mydisplay
