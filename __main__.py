import os
from pathlib import Path

#print('-----')
#print(Path(__file__).absolute().parent)
ImportProcess = False
working_directory = Path(__file__).absolute().parent
print(working_directory)
if ImportProcess:
  import subprocess
  from subprocess import Popen
  p = Popen(f"{working_directory}/initboot.bat", shell=True, stdout = subprocess.PIPE) # Auto-installs required dependancies
  stdout, stderr = p.communicate()

import unicurses
HOME_DIR  = os.getenv('UserProfile') if unicurses.OPERATING_SYSTEM == 'Windows' else os.getenv('HOME')
#tput init

print("Init boot complete")

Developer_Mode = True
#import OLD.playarea.py #OLD FILE

import engine.soundEngine
import engine.screenSetup

if Developer_Mode == True:
  print("Reached End of main script")

#py C:\Users\flint\PycharmProjects\CardGame\