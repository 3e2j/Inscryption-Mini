from unicurses import mvaddstr
from engine.screenSetup import sh, sw, gray
mvaddstr(sh//2,sw//2 - len("Loading...")//2, "Loading...", gray)
from engine.soundEngine import PlaySound,StopLoopingSound # When it loads this it has time to pre-init the sounds
from game.dialouge.waiting import waitTimerSecs
from game.dialouge.leshy import *
from game.dialouge.dialouge import clearLine
clearLine(0)

tutorial = False



# This is the main cabin that will be used for the remainer of rounds
def StartCabin():
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "cabin_ambience")
    global tutorial
    tutorial = True

    #PlaySound("stereo/cabin/gametable_ambience", 1, (0, 0, 0), "GametableAmbience")
    #sleep(3)
    #PlaySound("stereo/misc/eyes_opening", 0.8)
    #SetEyes("Opening")
    StartEyes()
    #waitTimerSecs(13)
    
    #leshyTalk("Another challenger... it has been ages.")
    #leshyTalk("Perhaps you have forgotton how this game is played.")
    #leshyTalk("Allow me to remind you.")

    #EngageBoard
    from game.gameboard import SelectCardFromDeck, startBoard
    startBoard()

    waitTimerSecs(1)

    #give squirrel + a low level card
    leshyTalk("Play the squirrel card.")
    SelectCardFromDeck()
    #Summon bell

    #Bell Ring
    #Engage combat
    leshyTalk("You may draw from your deck or you may draw a squirrel", skippable=True)
    #if takes power card then
    leshyTalk("How reckless of you.")

    #wait for player to make a move and ring bell
    leshyTalk("because you are learning I will pass.")
    #if use power card
    leshyTalk("The wolf demands two sacrifices.")

    leshyTalk("Fear not... the beast is sacrificed, but not removed from your deck")
    leshyTalk("It's suffering was real. But you will see it again.")
    #wait until turn
    leshyTalk("INSERT DAMAGE dealt, INSERT DAMAGE weights on the scale.")
    #while move
    leshyTalk("Pass.")
    #wait until completion
    leshyTalk("You've won this match.")
    leshyTalk("They won't all be so easy.")
    leshyTalk("Lets begin.")
    StopLoopingSound("cabin_ambience")
    PlaySound("stereo/cabin/gametable_ambience", 1, (0,0,0), "gametable_ambience")
    waitUntil("z",False)


StartCabin()