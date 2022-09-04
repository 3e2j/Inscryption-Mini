from game.dialouge.leshy import leshyTalk
from engine.soundEngine import PlaySound, StopLoopingSound
from time import sleep

from game.gameboard import \
    BellObject,\
    Scales,\
    PlaceCardOrColorChange

tutorialPhase = 0

'''
Game Events and triggers for doing certain actions. Contained in own Script to keep gameboard clean.
Will trigger certain events upon certain inputs. Mainly used for the tutorial section of the game.
'''

def GameEvents(dmgdealt=0):
    from game.gameboard import LastEvent, BoardID, IsTutorial # Reloads Last Event

    if IsTutorial:
        #Tutorial Section
        global tutorialPhase

        if tutorialPhase == 0:
            if LastEvent == 'CardPlacesquirrel':
                leshyTalk("Now play your lobster.")
            if LastEvent == 'positionPlacementlobster':
                leshyTalk("Lobster's require 1 sacrifice")
            if LastEvent == 'sacrifice':
                leshyTalk("An honorable death. Play the lobster.")
                tutorialPhase += 1

        if tutorialPhase == 1:
            if LastEvent == 'SelectCardFromDeck':
                leshyTalk("Wolves require two sacrifices. You do not have enough.")
                BellObject(spawn=True)
                leshyTalk("Ring the bell to end your turn... and commence combat.")
                tutorialPhase += 1

        if tutorialPhase == 2:
            if LastEvent == 'BellPressed':
                leshyTalk("Your lobster stands unopposed.")
                leshyTalk("The number on the bottom left is the attack power: 1.")
                Scales(scaleSpawn=True)
                #dealdmg
                sleep(0.3)
                tutorialPhase += 1

        if tutorialPhase == 3:
            if LastEvent == 'PlayerAttack':
                leshyTalk("Your lobster dealt me 1 damage. I added it to the scale")
                tutorialPhase += 1

        if tutorialPhase == 4:
            if LastEvent == 'ScaleTipPlayerAttack':
                leshyTalk("You win if you tip my side all the way down")
                from game.gameboard import scaleTip
                scaleTempStorage = scaleTip
                Scales(scaleWeight=4) #Tips scale
                leshyTalk("Like this.")
                Scales(scaleWeight=scaleTempStorage, scaleRefresh=True) # Refreshes back to original point
                sleep(1)
                leshyTalk("My turn.", skippable=True)
                sleep(2)

                # Plays card infront of placed card
                for cardPos in range(0,4): # find lobster placement
                    if not BoardID[2][cardPos] == "blankCardSpace":
                        from game.boardArt import coyote
                        PlaceCardOrColorChange(cardPos, 1, ["coyote", coyote[12], coyote[13], coyote[14]])
                        break
                sleep(2)
                leshyTalk("Your lobster stands in the way of my coyote.")
                tutorialPhase += 1

        if tutorialPhase == 5:
            if LastEvent == 'OpponentAttack':
                leshyTalk("My coyote dealt 2 damage to your lobster.")
                leshyTalk("That means your lobster's health is 2 less.")
                leshyTalk("If a creatures health reaches 0, it dies.")
                tutorialPhase += 1
        if tutorialPhase == 6:
            if LastEvent == 'ScaleTipOpponentAttack':
                leshyTalk("It's your turn again.")
                tutorialPhase += 1
        if tutorialPhase == 7:
            if LastEvent == 'DrawingCard':
                leshyTalk("You may draw from your deck or you may draw a squirrel", skippable=True)
                tutorialPhase += 1
        if tutorialPhase == 8:
            if LastEvent == 'DrewSquirrel':
                leshyTalk("How dull.", skippable=True)
                tutorialPhase += 1
            elif LastEvent == 'DrewPower':
                leshyTalk("How reckless of you.", skippable=True)
                tutorialPhase += 1
        if tutorialPhase == 9:
            if LastEvent == 'ScaleTipPlayerAttack':
                leshyTalk("because you are learning I will pass.")
            if LastEvent == 'RoundNotOverCheck': # makes sure it doesn't skip to 10 immediately
                tutorialPhase += 1
        if tutorialPhase == 10:
            if LastEvent == 'ScaleTipPlayerAttack':
                if dmgdealt == 1:
                    leshyTalk(f"{dmgdealt} damage dealt, {dmgdealt} weight on the scale.")
                else:
                    leshyTalk(f"{dmgdealt} damage dealt, {dmgdealt} weights on the scale.")
                tutorialPhase += 1
        if tutorialPhase == 11:
            if LastEvent == 'RoundNotOverCheck':
                leshyTalk("Pass.")
            if LastEvent == 'PlayerWin':
                leshyTalk("You've won this match.")
                leshyTalk("They won't all be so easy.")
                leshyTalk("Lets begin.")
                StopLoopingSound("cabin_ambience")
                PlaySound("stereo/cabin/gametable_ambience", 1, (0, 0, 0), "gametable_ambience")
    if LastEvent == "OpponentWinCandles":
        leshyTalk("You've lost this match...")
        leshyTalk("Where did I put that blastered thing?")
        leshyTalk("Here we go.", skippable=True)
        #ActivateCandles
        sleep(3)
        leshyTalk("Let me explain something to you.")
        #Put Out a Candle
        leshyTalk("That was one of the two mistakes you can make here.")
        leshyTalk("If you make another I must sacrifice you.")
        leshyTalk("Now, where were we...")