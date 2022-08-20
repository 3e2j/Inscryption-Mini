import os
import platform

SysOS = platform.system()

from pathlib import Path


ImportProcess = True
BypassLinuxRestriction = True # Won't support sound (used for my own end for programming)


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
    if not BypassLinuxRestriction:
      quit()

print("Init boot complete")

Developer_Mode = True
#import OLD.playarea.py #OLD FILE

if not BypassLinuxRestriction:
  import engine.soundEngine
import engine.screenSetup

if Developer_Mode == True:
  print("Reached End of main script")

#py C:\Users\flint\PycharmProjects\CardGame\