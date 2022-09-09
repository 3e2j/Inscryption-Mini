from engine.threadingEngine import threaded
from game.dialouge.dialouge import *
from game.dialouge.waiting import *
import time
from time import sleep

# Two threads are required due to running simultaniously.
@threaded
def dialouge(status):
    if status == "init":
        centreFadeIn("The game should be fullscreen. If you wish to exit this anytime, press F11 (Note: This will break the game)", -2, 0, 2)
    else:
        centreFadeOut("The game should be fullscreen. If you wish to exit this anytime, press F11 (Note: This will break the game)", -2, 0, 2)

@threaded
def dialouge2(status):
    if status == "init":
        centreFadeIn("It's recommended that you change your default terminal font size to 18 or below.", -1, 0, 2)
    else:
        centreFadeOut("It's recommended that you change your default terminal font size to 18 or below.", -1, 0, 2)

@threaded
def dialouge3(status):
    if status == "init":
        centreFadeIn("Press ENTER to continue", 0, 0, 2)
        dancingMan(1, 0, 0.5)
    else:
        centreFadeOut("Press ENTER to continue", 0, 0, 2)

@threaded
def dialouge4(status):
    if status == "init":
        centreFadeIn(" ┗(･o･ )┓ ", 1, 0, 2)
    else:
        centreFadeOut(" ┗(･o･ )┓ ", 1, 0, 2)
        sendWaitIdOrKey("DialougeSendOut")
        #exec("global DialougeSendOut \nDialougeSendOut = True")  # Quick line to push out a global value

@threaded
def dancingMan(heightChange, widthChange, TotalTime):
    while "DialougeSendIn" not in waitUntilKiller:
        centreDialougeX(" ┏(・o･)┛", heightChange, widthChange)
        sleep(TotalTime / 2)
        centreDialougeX(" ┗(･o･ )┓ ", heightChange, widthChange)
        sleep(TotalTime / 2)
    deleteKey("DialougeSendIn")

def StartGame():
    dialouge("init")
    dialouge2("init")
    dialouge3("init")
    dialouge4("init")
    from engine.soundEngine import PlaySound,StopLoopingSound, StopSoundList
    waitUntil("DialougeSendIn", ["^J"]) #^J represents enter (for some reason)
    dialouge("out")
    dialouge2("out")
    dialouge3("out")  # Assumes last thread therefore will have wait toggle (note: changes for time periods given)
    dialouge4("out")
    waitUntil("DialougeSendOut", False)
    clearLine(-2)
    clearLine(-1)
    clearLine(0)
    clearLine(1)