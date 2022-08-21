import os
import platform

SysOS = platform.system() #Grabs OS type

from pathlib import Path


ImportProcess = False #Determines if pre-setup is nessasary
Developer_Mode = True #Dev stats


working_directory = Path(__file__).absolute().parent #Grabs directory

if ImportProcess:
  import subprocess
  from subprocess import Popen
  if SysOS == 'Windows':
    p = Popen(f"{working_directory}/initboot.bat", shell=True, stdout = subprocess.PIPE) # Auto-installs required dependancies through initboot.bat
    stdout, stderr = p.communicate()
  else:
    print("Not supported on platforms other then Windows.") #Could be replaced with a open file for initboot.sh, haven't worked out how to get all files installed yet.
    quit()

if Developer_Mode:
  print("Init boot complete")

import keyboard

keyboard.press_and_release("f11") #Makes the game full-screen before assigning xy dimentions to Curses

'''
If you wish to see the original prototype of the game, enable this file.
Note: It wasn't finished and did not run through Curses, just base Python.
'''
#import old.playarea.py

import engine.screenSetup

if Developer_Mode == True:
  print("Reached End of main script")
os._exit(1)
#py C:\Users\flint\PycharmProjects\CardGame\