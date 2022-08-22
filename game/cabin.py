from engine.soundEngine import PlaySound,StopLoopingSound, StopSoundList
from game.dialouge.dialouge import waitTimerSecs
from game.dialouge.leshy import *
import unicurses

# This is the main cabin that will be used for the remainer of rounds
def StartCabin():
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "CabinAmbience")
    sleep(3)
    PlaySound("stereo/misc/eyes_opening", 0.8)
    SetEyes("Opening")
    StartEyes()
    waitTimerSecs(15)
    leshyTalk("Another challenger... it has been ages.")
    while True: # dev loop to stop quit
        unicurses.mvaddstr(17,0,f"{eyesStatus}")
        unicurses.refresh()


StartCabin()