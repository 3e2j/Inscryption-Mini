from unicurses import mvaddstr
from engine.screenSetup import sh, sw, gray
mvaddstr(sh//2,sw//2 - len("Loading...")//2, "Loading...", gray)
from engine.soundEngine import PlaySound # When it loads this it has time to pre-init the sounds
from game.dialouge.waiting import waitTimerSecs
from game.dialouge.leshy import *
from game.dialouge.dialouge import clearLine
clearLine(0)





# This is the main cabin that will be used for the remainer of rounds
def StartCabin():
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "cabin_ambience")
    #sleep(3)
    #PlaySound("stereo/misc/eyes_opening", 0.8)
    #SetEyes("Opening")
    StartEyes()
    #waitTimerSecs(13)
    
    #leshyTalk("Another challenger... it has been ages.")
    #leshyTalk("Perhaps you have forgotton how this game is played.")
    #leshyTalk("Allow me to remind you.")

    #EngageBoard
    from game.gameboard import startBoard, StartGame
    #startBoard()

    waitTimerSecs(1)

    leshyTalk("Play the squirrel card.")
    StartGame()
    #StartGame(True)


StartCabin()