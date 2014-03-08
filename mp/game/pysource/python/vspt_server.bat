:: Get game dir by going into the directory with the gameinfo.txt and capturing %CD%
:: This is based on the assumption the "vspt" script is placed in the python sub folder of the game/mod
cd "%~dp0"
cd ..
Set GAMEDIR="%CD%"

:: Get steam dir
Set Reg.Key=HKEY_CURRENT_USER\Software\Valve\Steam
Set Reg.Val=SteamPath

For /F "Tokens=2*" %%A In ('Reg Query "%Reg.Key%" /v "%Reg.Val%" ^| Find /I "%Reg.Val%"' ) Do Call Set STEAMDIR=%%B

:: Change working directory to Source SDK Base 2013 Multiplayer
cd "%STEAMDIR%\SteamApps\common\Source SDK Base 2013 Multiplayer\bin"
echo %GAMEDIR%
:: Set game executable
SET GAMEEXE="%STEAMDIR%\steamapps\common\Source SDK Base 2013 Multiplayer\hl2.exe"

:: Launch in text mode with the -interpreter option (must be at the back)
%GAMEEXE% -dev -textmode -sw -noborder -game %GAMEDIR% -interpreter %*
