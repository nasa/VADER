 Volume_Up::
	Run C:\Python27\pythonw.exe C:\vaderScripts\serial-volumeUP.py 3
	return
Volume_Down::
	Run C:\Python27\pythonw.exe C:\vaderScripts\serial-volumeDOWN.py 3
	return
Volume_Mute::
	Run C:\Python27\pythonw.exe C:\vaderScripts\serial-volumeMUTE.py 3
	return
+F3::
	Run C:\Python27\pythonw.exe C:\vaderScripts\serial-POWER.py 3
	return
CapsLock::
	;Run C:\Python27\pythonw.exe C:\vaderScripts\serial-switchPC.py 
		
IfWinActive XBMC
{
	;sc130::Send {+} ; Volume Up => +
	;sc12E::Send {-} ; Volume Down => -
	;Volume_Mute::Send {-} ; Volume Down
	;Sleep::Send {+} ; Volume Up
}
Return