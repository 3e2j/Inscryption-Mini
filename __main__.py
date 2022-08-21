import os
import platform

SysOS = platform.system()

from pathlib import Path


ImportProcess = False
Developer_Mode = True


working_directory = Path(__file__).absolute().parent
print(working_directory)
if ImportProcess:
  import subprocess
  from subprocess import Popen
  if SysOS == 'Windows':
    p = Popen(f"{working_directory}/initboot.bat", shell=True, stdout = subprocess.PIPE) # Auto-installs required dependancies
    stdout, stderr = p.communicate()
  else:
    print("Not supported on platforms other then Windows.")
    quit()

print("Init boot complete")

import keyboard

#keyboard.press_and_release("f11")


#import OLD.playarea.py #OLD FILE

#import engine.soundEngine
import engine.screenSetup

if Developer_Mode == True:
  print("Reached End of main script")
os._exit(1)
#py C:\Users\flint\PycharmProjects\CardGame\