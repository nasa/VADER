; Script Function:
;	Restarts XBMC if it hasn't started 
;
;   This script loops every (15) seconds to determine if XBMC is running or not, and restarts it if it's not.
;

#SingleInstance, force
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.

XBMC_EXE     = C:\\Program Files\\XBMC\\XBMC.exe
XBMC_Path    = C:\\Program Files\\XBMC
XBMC_imgName = XBMC.exe

loop 
{
	sleep 15000
	Send {Space}
	Process, Exist, %XBMC_imgName% ; check to see if XBMC is running
	If (ErrorLevel = 0) ; If it is not running
	{
		Run, %XBMC_EXE%
	}
	Else ; If it is running, ErrorLevel equals the process id for XBMC. Check for hung window.
	{
		IfWinExist, XBMC
		{
			if DllCall("IsHungAppWindow", "Uint", WinExist())
			{
				Send {Space} 
				Process,Close,XBMC.exe
			}
		}
	sleep 5
	}
}

