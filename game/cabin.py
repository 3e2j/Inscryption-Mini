from engine.soundEngine import PlaySound#,StopLoopingSound, StopSoundList
from game.dialouge.waiting import waitTimerSecs
from game.dialouge.leshy import *

tutorial = False



# This is the main cabin that will be used for the remainer of rounds
def StartCabin():
    sleep(0.5)
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "CabinAmbience")
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
    from game.gameboard import SelectCardFromDeck, startBoard, BellObject
    startBoard()

    waitTimerSecs(1)

    #give squirrel + a low level card
    leshyTalk("Play the squirrel card.")
    SelectCardFromDeck()
    #Summon bell

    #Bell Ring
    leshyTalk("Your stoat stands unopposed.")
    leshyTalk("The number on the bottom left is the attack power: 1.")
    #Engage combat
    leshyTalk("Your stoat dealt 1 damage. I added it to the scale.")
    leshyTalk("You win if you tip my side all the way down")
    #tipping
    leshyTalk("Like this.")
    leshyTalk("My turn.", skippable=True)
    #Play coyote ON MID
    leshyTalk("Your stoat stands in the way of my coyote.")
    #deal dmg
    leshyTalk("My cyotote dealt 2 damage to your stoat.")
    leshyTalk("That means your stoat's health is 2 less.")
    leshyTalk("If a creatures health reaches 0, it dies.")
    leshyTalk("It's your turn again.")
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
    #StopLoopingSound("CabinAmbience")
    PlaySound("stereo/cabin/gametable_ambience", 1, (0,0,0), "GametableAmbience")
    waitUntil("z",False)


StartCabin()