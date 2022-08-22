import os
import sys


Developer_Mode = True #Dev stats


import subprocess
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("uni-curses")
install("pyogg")

install("PyOpenAL")
install("pynput")
install("pathlib")

import platform
SysOS = platform.system() #Grabs OS type

from pathlib import Path

working_directory = Path(__file__).absolute().parent #Grabs directory

# try:
#   f = open("save-file.txt", "x")
#   f.write("ImportProcess = Complete")
#   import subprocess
#   from subprocess import Popen
#   if SysOS == 'Windows':
#     p = Popen(f"{working_directory}/initboot.bat", shell=True, stdout = subprocess.PIPE) # Auto-installs required dependancies through initboot.bat
#     stdout, stderr = p.communicate()
#   else:
#     pass
#   f.close

# except:
#   print("Import process has run before\nIf the game is not running, ignore this message.\nIf it's not running and you wish to retry imports, delete save-file.txt")
#   pass

if Developer_Mode:
  print("Init boot complete")

from pynput.keyboard import Key, Controller

keyboard = Controller()

keyboard.press(Key.f11)
keyboard.release(Key.f11)

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