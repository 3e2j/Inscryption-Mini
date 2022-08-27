import os
import sys


Developer_Mode = True #Dev stats
TurnOffSoundForLinux = False # Dev command (LINUX NOT SUPPORTED)

import subprocess
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    x = open("save-file.txt", "x")
    install("uni-curses")
    install("pyogg")
    install("PyOpenAL")
    install("pynput")
    install("pathlib")
    x.write("ImportProcess = True")
except:
    pass

import platform
SysOS = platform.system() #Grabs OS type

from pathlib import Path

working_directory = Path(__file__).absolute().parent #Grabs directory

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