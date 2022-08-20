from threading import Thread
from time import sleep

def soundEngineStart():
  print("RUNNING SOUND THREAD")
  import soundEngine
  pass
def gameBoardStart():
  print("RUNNING GAME BOARD THREAD")
  #import game.gameBoard
  import game.gameBoard
  pass

sleep(0.2) # Check that booting is working

soundINIT = Thread(target=soundEngineStart)
gameBoardINIT = Thread(target=gameBoardStart)


try:
  #sountINIT.start()
  gameBoardINIT.start()
  #sountINIT.join()
  gameBoardINIT.join()
  print("Finished Threading Setup")
except:
  print("Error, Unable to initalise threading - Backbone file.")