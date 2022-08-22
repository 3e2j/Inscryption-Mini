# This is the main cabin that will be used for the remainer of rounds
from engine.soundEngine import PlaySound,StopLoopingSound, StopSoundList
from game.dialouge.dialouge import waitTimerSecs
from game.dialouge.eyes import *
import unicurses

def StartCabin():
    #PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "CabinAmbience")
    #sleep(3)
    PlaySound("stereo/misc/eyes_opening", 0.8)
    SetEyes("Opening")
    StartEyes()
    while True:
        unicurses.mvaddstr(12,0,f"{eyesStatus}")
        unicurses.refresh()
    waitTimerSecs(7)
    unicurses.mvaddstr(12, 0, f"Wait time complete")
    waitTimerSecs(7)


StartCabin()