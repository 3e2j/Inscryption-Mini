from engine.soundEngine import PlaySound,StopLoopingSound, StopSoundList
from game.dialouge.waiting import waitTimerSecs
from game.dialouge.leshy import *

from game.gameboard import SelectCardFromDeck, startBoard, BellObject


# This is the main cabin that will be used for the remainer of rounds
def StartCabin():
    PlaySound("stereo/cabin/cabin_ambience", 1, (0,0,0), "CabinAmbience")
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
    startBoard()

    waitTimerSecs(1)

    #give squirrel + a low level card
    leshyTalk("Play the squirrel card.")
    BellObject(spawn=True)
    SelectCardFromDeck()
    #PlaceCard(4,2,"lobster")

    leshyTalk("Now play your stoat.")
    SelectCardFromDeck()
    leshyTalk("Stoats cost 1 blood. Sacrifices must be made.")
    leshyTalk("An honorable death. Play the stoat.")
    SelectCardFromDeck()
    leshyTalk("Wolves require two sacrifices. You do not have enough.")
    #Summon bell
    leshyTalk("Ring the bell to end your turn... and commence combat.")
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
    PlaySound("stereo/cabin/gametable_ambience", 1, (0,0,0), "GametableAmbience")
    waitUntil("z",False)


StartCabin()