Volume_Up::
	Run C:\Python27\pythonw.exe C:\vaderScripts\mococenSerial\serial-volumeUP.py
	return
Volume_Down::
	Run C:\Python27\pythonw.exe C:\vaderScripts\mococenSerial\serial-volumeDOWN.py
	return
Volume_Mute::
	Run C:\Python27\pythonw.exe C:\vaderScripts\mococenSerial\serial-volumeMUTE.py
	return
+F3::
	Run C:\Python27\pythonw.exe C:\vaderScripts\mococenSerial\serial-POWER.py
	return
CapsLock::
	;Run C:\Python27\pythonw.exe C:\vaderScripts\mococenSerial\serial-switchPC.py
		
IfWinActive XBMC
{
	;sc130::Send {+} ; Volume Up => +
	;sc12E::Send {-} ; Volume Down => -
	;Volume_Mute::Send {-} ; Volume Down
	;Sleep::Send {+} ; Volume Up
}
Return