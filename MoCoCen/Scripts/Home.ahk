Home::

Run C:\Python27\pythonw C:\vaderScripts\mococenSerial\serial-POWERON.py
sleep 100

Send {Space}  
;SoundPlay, C:\vaderScripts\Darth_Vader.wav
   
SetTitleMatchMode, 2
IfWinExist, MimioStudio Notebook
{
	WinKill
	Send {Down}
	Send {Space}
} 

SetTitleMatchMode, 3
IfWinExist, XBMC
{
	WinActivate
	Send {Home}
}
else
{
	Run "C:\\Program Files\\XBMC\\XBMC.exe"
}

WinGet, Style, Style, ahk_class XBMC
if (Style & 0xC00000)  ;Detects if XBMC has a title bar.
{
	Send {VKDC}  ;Maximize XBMC to fullscreen mode if its in a window mode.
}


