import os
import platform

SysOS = platform.system() #Grabs OS type

from pathlib import Path


Developer_Mode = True #Dev stats


working_directory = Path(__file__).absolute().parent #Grabs directory

try:
  f = open("save-file.txt", "x")
  f.write("ImportProcess = Complete")
  import subprocess
  from subprocess import Popen
  if SysOS == 'Windows':
    p = Popen(f"{working_directory}/initboot.bat", shell=True, stdout = subprocess.PIPE) # Auto-installs required dependancies through initboot.bat
    stdout, stderr = p.communicate()
  else:
    pass
  f.close

except:
  print("Import process has run before\nIf the game is not running, ignore this message.\nIf it's not running and you wish to retry imports, delete save-file.txt")
  pass

if not SysOS == 'Windows':
    print("NOTICE: Not supported on platforms other then Windows.")
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