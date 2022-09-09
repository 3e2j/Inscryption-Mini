from unicurses import mvaddstr
from engine.screenSetup import sh, sw, gray
mvaddstr(sh//2,sw//2 - len("Loading...")//2, "Loading...", gray)
from engine.soundEngine import PlaySound # When it loads this it has time to pre-init the sounds
from game.dialouge.waiting import waitTimerSecs
from game.dialouge.leshy import *
from game.dialouge.dialouge import clearLine
from __main__ import working_directory
from game.gameboard import startBoard, StartTheGame
clearLine(0)





# This is the main cabin that will be used for the remainer of rounds
def StartCabin():

    def engageTutorial():
        leshyTalk("Another challenger... it has been ages.")
        leshyTalk("Perhaps you have forgotton how this game is played.")
        leshyTalk("Allow me to remind you.")

        # EngageBoard
        startBoard()

        waitTimerSecs(1)

        leshyTalk("Play the squirrel card.")
        StartTheGame(True)

    from game.startScreen import engageStartScreen
    engageStartScreen()
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "cabin_ambience")
    sleep(3)
    PlaySound("stereo/misc/eyes_opening", 0.8)
    #SetEyes("End")
    SetEyes("Opening")
    StartEyes()
    waitTimerSecs(13)

    with open(f"{working_directory}/save-file.txt", "r") as saveFile:
        lines = saveFile.readlines()
        saveFile.close()
    if "tutorialCompleted = True" in lines:
        from random import choice
        leshyTalk(choice(["So you have returned,", "How nice to see you once again.", "Welcome back."]))
        leshyTalk(choice(["Let us begin.", "A new match is to be set.", "I suppose that you fancy a new match?"]))
        startBoard()
        StartTheGame()
    else:
        engageTutorial()


StartCabin()