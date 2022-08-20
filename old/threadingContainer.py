import threading
from time import sleep
from engine.screenSetup import StandardScreen
from __main__ import Developer_Mode

RunningThreads = {}


#Commands that don't run via functions
def SingleFunction(Command):
  try:
    Command
  except:
    pass

def ThreadingLooper(Target, BeingThreaded):
  StandardScreen.addstr(5, 0, f"{RunningThreads}")
  try:
    while RunningThreads[Target]:
          BeingThreaded.start()
          BeingThreaded.join() # Checks that thread is completed
  except:
    StandardScreen.addstr(3, 0, f"Thread killed {Target}, {BeingThreaded}")

def ThreadingStartup(Target, Loop, *innerArgs):

#Initalise the Thread
  BeingThreaded = threading.Thread(target=Target, args = innerArgs)
  if Target == False: # Call to say functions doesn't exist (SingleFunction)
    BeingThreaded = threading.Thread(target=SingleFunction, args = innerArgs)

#Basic Thread
  if Loop == False:
    try:
      RunningThreads[Target] = True
      if Developer_Mode == True:
        StandardScreen.addstr(5, 0, f"{RunningThreads}")
      BeingThreaded.start()
    except:
      if Developer_Mode == True:
        StandardScreen.addstr(2, 0, f"ERROR, Unable to initalise threading {Target}, {BeingThreaded}")


#Looping Thread
  else:
    ThreadLooper = threading.Thread(target=ThreadingLooper, args = [Target,BeingThreaded])
    try:
      RunningThreads[Target] = True
      ThreadLooper.start()
    except:
      if Developer_Mode == True:
        StandardScreen.addstr(2, 0, f"ERROR, Unable to initalise threading {Target}, {BeingThreaded}")

#Developer Debugging Info
  if Developer_Mode == True and BeingThreaded.isAlive():
    StandardScreen.addstr(2, 0, f"Successful Threading Setup for {Target}, {BeingThreaded}")
  elif Developer_Mode == True and not BeingThreaded.isAlive():
    StandardScreen.addstr(2, 0, f"Unsuccesful Threading Setup for {Target}, {BeingThreaded}")

#ThreadKiller (Toggle to stop when reach end)
def ThreadingKiller(Target):
  del RunningThreads[Target]


#### Problem is that it doesn't actually thread everything: It threads the files and thats great and all but it doesnt return the script because it cant.

#Call ThreadingWrapper whenever needing to init a wrapper