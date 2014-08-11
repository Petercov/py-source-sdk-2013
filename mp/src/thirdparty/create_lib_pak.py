import os
import subprocess

basescript = r'''
rem @echo off

@rem Get steam dir
Set Reg.Key=HKEY_CURRENT_USER\Software\Valve\Steam
Set Reg.Val=SteamPath

For /F "Tokens=2*" %%A In ('Reg Query "%Reg.Key%" /v "%Reg.Val%" ^| Find /I "%Reg.Val%"' ) Do Call Set steamdir=%%B
echo %steamdir%

PATH=PATH;"%steamdir%/SteamApps/common/Source SDK Base 2013 Multiplayer/bin"
'''



target_folders = ['python/lib']
file_types = ['.py']

response_path = os.path.join(os.getcwd(),"vpk_list.txt")
script_path = os.path.join(os.getcwd(),"vpk_script.bat")

len_cd = len(os.getcwd()) + 1
 
with open(response_path,'wt') as fp:
    for user_folder in target_folders:
        for root, dirs, files in os.walk(os.path.join(os.getcwd(),user_folder)):
            for file in files:
                #if len(file_types) and file.rsplit(".")[-1] in file_types:
                fp.write(os.path.join(root[len_cd:].replace("/","\\"),file) + "\n")
                    
with open(script_path, 'wt') as fp:
    fp.write(basescript)
    fp.write('cd %s\n' % os.getcwd())
    fp.write('vpk.exe -M a pysource_lib "@%s"' % response_path)
subprocess.call([script_path])