from unicurses import mvaddstr
from engine.screenSetup import sh,sw,white,dark_gray,mediocre_gray, gray,brightorange,red, ResetKey
from game.dialouge.leshy import leshyTalk
from time import sleep
from __main__ import Developer_Mode
from random import choice

from engine.threadingEngine import threaded


from game.BoardArt import \
    bell, \
    blankCardSpace, \
    bigblank, \
    lobster, \
    biglobster, \
    lobster2, \
    biglobster2, \
    squirrel, \
    bigsquirrel, \
    wolf, \
    bigwolf

from engine.soundEngine import PlaySound

from array import *

BoardID = [
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#0
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#1
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"]#2
    ]
deck = [] # Users current GAME deck of cards
LastEvent = "" #CardPlace{TYPE}, positionPlacement{TYPE},sacrifice,SelectCardFromDeck,BellPressed, BellSpawn

tutorialPhase = 0

from game.cabin import tutorial

def leshyTutorialChecker():
    mvaddstr(19,0,LastEvent)
    global tutorialPhase
    if tutorialPhase == 0:
        if LastEvent == 'CardPlacesquirrel':
            leshyTalk("Now play your lobster.")
        if LastEvent == 'positionPlacementlobster':
            leshyTalk("Lobster's require 1 sacrifice")
        if LastEvent == 'sacrifice':
            leshyTalk("An honorable death. Play the lobster.")
        if LastEvent == 'CardPlacelobster':
            deck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
            deck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
            leshyTalk("Wolves require two sacrifices. You do not have enough.")
            BellObject(spawn=True)
            leshyTalk("Ring the bell to end your turn... and commence combat.")
            tutorialPhase += 1


def startBoard():
    cardCentringOriginal = -38
    soundPositionOriginal = -0.2
    cardHeight = -15
    for cardRow in range(0,3):
        cardCentering = cardCentringOriginal
        soundPosition = soundPositionOriginal
        for card in range(0,4):
            mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, blankCardSpace[0], white)
            heightAddition = 1
            for line in range(0,10):
                mvaddstr(sh // 2 + cardHeight + heightAddition, sw // 2 + cardCentering, blankCardSpace[1], white)
                heightAddition += 1
            heightAddition = 0
            mvaddstr(sh // 2 + cardHeight +11, sw // 2 + cardCentering, blankCardSpace[11], white)
            cardCentering += 20
            CardPlaySound("glow",(soundPosition, 0,1))
            soundPosition += 0.1
            sleep(0.2)
        cardHeight += 12
    global BoardID
    BoardID = [
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#0
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#1
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"]#2
    ]
    deck.append(["squirrel",squirrel[12],squirrel[13], squirrel[14]]) # type, attack, health, blood #NOTE THIS IS THE ONLY TIME THAT THE DEFAULT NUMBERS ARE USED
    deck.append(["lobster", lobster[12], lobster[13], lobster[14]])  # type, attack, health, blood

    if Developer_Mode:
        #mvaddstr(22, 0, BoardID)
        mvaddstr(59,0,deck)

reference = {
        "bell" : bell,
        "blankCardSpace" : blankCardSpace,
        "bigblank" : bigblank,
        "lobster" : lobster,
        "biglobster" : biglobster,
        "lobster2": lobster2,
        "biglobster2": biglobster2,
        "squirrel" : squirrel,
        "bigsquirrel": bigsquirrel,
        "wolf": wolf,
        "bigwolf": bigwolf
    }



bellEnabled = False




def PlaceCardOrColorChange(cardNum, row, deckCardInfo, placement = True, color = white): #Updates to board

    cardCentering = -38 + (20 * cardNum) #Centering; changes 1-4 to 0-3
    soundPosition = -0.2
    cardHeight = -15 + (12 * row) #Height; changes 1-3 to 0-2

    if deckCardInfo == "blankCardSpace":
        mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, blankCardSpace[0], color)
        cardHeight += 1
        for _ in range(0,10):
            mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, blankCardSpace[1], color)
            cardHeight += 1
        mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, blankCardSpace[11], color)
    else:
        CardType = deckCardInfo[0]
        mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, reference[CardType][0], color)  # Drawing out the card
        mvaddstr(sh // 2 + cardHeight + 1, sw // 2 + cardCentering, reference[CardType][1], color)
        mvaddstr(sh // 2 + cardHeight + 2, sw // 2 + cardCentering, reference[CardType][2], color)
        mvaddstr(sh // 2 + cardHeight + 3, sw // 2 + cardCentering, reference[CardType][3], color)
        mvaddstr(sh // 2 + cardHeight + 4, sw // 2 + cardCentering, reference[CardType][4], color)
        mvaddstr(sh // 2 + cardHeight + 5, sw // 2 + cardCentering, reference[CardType][5], color)
        mvaddstr(sh // 2 + cardHeight + 6, sw // 2 + cardCentering, reference[CardType][6], color)
        mvaddstr(sh // 2 + cardHeight + 7, sw // 2 + cardCentering, reference[CardType][7], color)
        mvaddstr(sh // 2 + cardHeight + 8, sw // 2 + cardCentering, reference[CardType][8], color)
        mvaddstr(sh // 2 + cardHeight + 9, sw // 2 + cardCentering, reference[CardType][9], color)
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering, reference[CardType][10], color)
        mvaddstr(sh // 2 + cardHeight + 11, sw // 2 + cardCentering, reference[CardType][11], color)
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 2, f"{deckCardInfo[1]}†", color)  # Attack
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 13, f"{deckCardInfo[2]}♥", color)  # Attack
        if color == white:
            color = red
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 9 - deckCardInfo[3], "δ" * deckCardInfo[3],color)  # Attack
    if placement:
        CardPlaySound("normal",(soundPosition+(0.1*cardNum), 0, 1))
        global BoardID
        BoardID[row][cardNum] = [CardType,deckCardInfo[1],deckCardInfo[2],deckCardInfo[3]]

def printSideBig(deckCardInfo, color, blank=False): # Prints preview of deck on right-hand side of screen
    if blank == True:
        count = 0
        for _ in range (0,31):
            mvaddstr(sh // 2 - 12 + count, sw // 2 + 58, bigblank[0], color)
            count += 1
    else:
        count = 0
        portrait = f"big{deckCardInfo[0]}"
        for _ in range(0,31):
            mvaddstr(sh // 2 -12 + count, sw // 2 + 58, reference[portrait][count], color)
            count +=1
        mvaddstr(sh // 2 - 12 + 28, sw // 2 + 64, f"{deckCardInfo[1]}†", color)
        mvaddstr(sh // 2 - 12 + 28, sw // 2 + 90, f"{deckCardInfo[2]}♥", color)
        if color == white:
            color = red
        mvaddstr(sh // 2 -10, sw // 2 + 90 - deckCardInfo[3], "δ" * deckCardInfo[3], color)

def positionPlacement(oldSelect=0, spectating = False): # Position on one of the 4 avaliable places to put a card (Includes sacrifices)

    global LastEvent
    try:
        LastEvent = f"positionPlacement{deck[oldSelect][0]}"
    except:
        LastEvent = f"positionPlacementnone"
    if tutorial:
        leshyTutorialChecker()

    placementCount = 0
    sacrificeRequired = False
    sacrificeMade = False
    bellSelected = False
    bellPressed = False
    placing = False
    SelectCardReturn = False
    wU = True # Looper
    from game.dialouge.dialouge import clearLine
    sacrifices = []
    posCenter = -30
    while wU:
        def changeOldCardToWhite(placement=BoardID[2][placementCount], cardNum = placementCount, ignoreCard=False):
            if not ignoreCard:
                PlaceCardOrColorChange(cardNum, 2, placement, False, white)
            if cardNum == -1:
                mvaddstr(sh // 2 + 13 + 9, sw // 2 - 66, " ", brightorange)
            else:
                mvaddstr(sh // 2 + 21, sw // 2 + posCenter + (20 * cardNum), " ", brightorange)

        ResetKey()
        try:
            if deck[oldSelect][3] > 0 and not sacrificeMade and not spectating and not bellSelected: # Checks if a sacrifice is being made
                sacrificeRequired = True
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, red)
            elif not bellSelected: # No sacrifice could be made
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
                placing = True
        except: # Empty deck exception
            if not bellSelected:
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
                placing = True
        if not placementCount == -1: #normal
            mvaddstr(sh // 2 + 21 ,sw // 2 + posCenter + (20 * placementCount),"^", brightorange)
        else: # bell
            mvaddstr(sh // 2 + 13 + 9, sw // 2 -66, "^", brightorange)


        checkInput = True
        while checkInput:
            from engine.screenSetup import key
            if not placementCount - 1 <= -1: # Not Bell
                if key == "KEY_LEFT" or key == "a":
                    if not placementCount in sacrifices:
                        changeOldCardToWhite()
                    placementCount -= 1
                    checkInput = False
            else: # Bell
                if not placementCount -1 == -2 and bellEnabled and spectating: #cant go over bell
                    if key == "KEY_LEFT" or key == "a":
                        changeOldCardToWhite()
                        bellSelected = True
                        placementCount -= 1
                        BellObject(white)
                        checkInput = False

            if not placementCount + 1 == 4:
                if key == "KEY_RIGHT" or key == "d":
                    if not placementCount + 1 == 0: # cant go over board
                        if not placementCount in sacrifices:
                            changeOldCardToWhite()
                        placementCount += 1
                        checkInput = False
                    else: # If on bell, turn it off
                        changeOldCardToWhite(ignoreCard=True)
                        BellObject(gray)
                        bellSelected = False
                        placementCount += 1
                        checkInput = False

            if (key == "^[" or key == "x" or key == 's' or key == "KEY_DOWN") and not sacrificeMade:
                if not sacrifices == []:
                    for position in sacrifices:
                        changeOldCardToWhite(BoardID[2][position], position)

                if not bellSelected:
                    changeOldCardToWhite()
                else:
                    changeOldCardToWhite(ignoreCard=True)
                SelectCardReturn = True
                checkInput = False
                wU = False
            if (key == "^J" or key == 'z'):
                checkInput = False
                if bellSelected and spectating:
                    bellPressed = True
                    wU = False
                elif placing and BoardID[2][placementCount] == "blankCardSpace" and not spectating and not deck == []: # Will not continue if sacrifice is not made
                    wU = False
                if sacrificeRequired and not sacrificeMade and not BoardID[2][placementCount] == "blankCardSpace" and not placementCount in sacrifices and not spectating:
                    sacrifices.append(placementCount) #appends position of sacrifice
                    PlaySound("mono/card/sacrifice_mark",0.7,(-0.2+(0.1*placementCount),0,1))
                    if len(sacrifices) == deck[oldSelect][3]:
                        for position in sacrifices:
                            BoardID[2][position] = "blankCardSpace"
                            PlaySound("mono/card/sacrifice_default", 0.7, (-0.2 + (0.1 * position), 0, 1))
                            changeOldCardToWhite(BoardID[2][position], position)

                            LastEvent = "sacrifice"
                            if tutorial:
                                leshyTutorialChecker()

                        sacrifices.clear()
                        sacrificeMade = True
                        sacrificeRequired = False
                        placing = True
                elif sacrificeRequired and not sacrificeMade and BoardID[2][placementCount] == "blankCardSpace":
                    leshyTalk(f"The {reference[deck[oldSelect][0]][15]} requires {deck[oldSelect][3]} blood.", skippable=True)
    if SelectCardReturn:
        clearLine(21)
        SelectCardFromDeck(oldSelect)
    else:
        if bellPressed:
            changeOldCardToWhite(ignoreCard=True)
            try:
                printSideBig(deck[0], gray)
            except:
                printSideBig(None, None, True)
            BellObject(pressed=True)
        else:
            PlaceCardOrColorChange(placementCount, 2, deck[oldSelect])
            changeOldCardToWhite(ignoreCard=True)
            tempStoreOldTitle = deck[oldSelect][0]
            deck.pop(oldSelect)
            try:
                printSideBig(deck[0], gray)
            except:
                printSideBig(None, None, True)

            LastEvent = f"CardPlace{tempStoreOldTitle}"
            if tutorial:
                leshyTutorialChecker()


            if deck == []: # spectator mode sendback
                leshyTalk("It seems you are out of cards. How unfortunate.", tone="curious", skippable=True)
                SelectCardFromDeck(0, True)

            else: #repeat
                sleep(0.4)
                SelectCardFromDeck()

import unicurses

#First in the event of the players turn, allows a selection from their current deck.
def SelectCardFromDeck(count=0, turnOffArrows=False):

    global LastEvent
    LastEvent = "SelectCardFromDeck"


    if not turnOffArrows and not deck == []:
        wU = True
        while wU:
            ResetKey()
            canGoLeft = False
            canGoRight = False
            printSideBig(deck[count], white)
            #Place marker indicating left/right avaliability
            if not count -1 == -1:
                mvaddstr(sh // 2 + 2, sw // 2 + 55, "<", brightorange)
                canGoLeft = True
            else:
                mvaddstr(sh // 2 + 2, sw // 2 + 55, "<", gray)
            try:
                if deck[count+1]:
                    mvaddstr(sh // 2 + 2, sw // 2 + 99, ">", brightorange)
                    canGoRight = True
            except:
                mvaddstr(sh // 2 + 2, sw // 2 + 99, ">", gray)

            checkInput = True

            while checkInput == True:
                #Grab key
                from engine.screenSetup import key
                if canGoLeft and key == "KEY_LEFT" or key == "a":
                    count -= 1
                    checkInput = False
                if canGoRight and key == "KEY_RIGHT" or key == "d":
                    count += 1
                    checkInput = False
                if key == "w" or key == "KEY_UP":
                    printSideBig(deck[count], gray)  # Gray's out the portrait to show selected
                    positionPlacement(spectating=True)  # Moves onto placement
                    checkInput = False
                    wU = False
                if key == "^J" or key == 'z':
                    printSideBig(deck[count], brightorange)  # Gray's out the portrait to show selected
                    positionPlacement(count, False)  # Moves onto placement
                    checkInput = False
                    wU = False

                    if tutorial:
                        leshyTutorialChecker()


    else:
        mvaddstr(sh // 2 + 2, sw // 2 + 55, " ")
        mvaddstr(sh // 2 + 2, sw // 2 + 99, " ")
        printSideBig(None, None, True)
        positionPlacement(spectating=True)

def BellObject(color = gray, spawn=False, pressed = False):
    global LastEvent
    if spawn:

        LastEvent = "BellSpawn"
        if tutorial:
            leshyTutorialChecker()

        PlaySound("mono/bell/combatbell_enter",0.8,(-0.3,0,0.8))
        def spawnBell():
            count = 0
            for _ in range(0,12):
                mvaddstr(sh // 2 + count + 9, sw // 2 -80, bell[count], color)
                count +=1
            count = 0
            sleep(0.15)
        color = dark_gray
        spawnBell()
        color = mediocre_gray
        spawnBell()
        color = gray
        spawnBell()
        global bellEnabled
        bellEnabled = True
    else:
        def NotPressed():
            count = 0
            for _ in range(0,12):
                mvaddstr(sh // 2 + count + 9, sw // 2 -80, bell[count], color)
                count +=1
        @threaded
        def Pressed():
            count = 0
            mvaddstr(sh // 2 + count + 9, sw // 2 - 80, bell[13], color) # clear top
            mvaddstr(sh // 2 + count + 1 + 9, sw // 2 - 80, bell[count], color) #push
            count += 2
            for _ in range(0,10):
                mvaddstr(sh // 2 + count + 9, sw // 2 -80, bell[count], color) # rest of bell
                count +=1

        if pressed:

            LastEvent = 'BellPressed'
            if tutorial:
                leshyTutorialChecker()

            color = gray
            Pressed()
            PlaySound("mono/bell/combatbell_ring",0.8,(-0.3,0,0.8))
            sleep(0.5)
            NotPressed()
            #Commense opponents turn
        else:
            NotPressed()



def CardPlaySound(tone="normal", position=(0,0,0)):
    if tone == "normal":
        normal = [
            "card#1",
            "card#2",
            "card#3",
            "card#4",
            "card#5",
            "card#6",
            "card#7",
            "card#8",
            "card#9",
            "card#10"
        ]
        PlaySound(f"mono/card/{choice(normal)}", 0.7, position)
    if tone == "quick":
        quick = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{choice(quick)}", 0.7, position)
    if tone == "glow":
        glow = [
            "cardslot_glow#1",
            "cardslot_glow#2",
            "cardslot_glow#3",
            "cardslot_glow#4"
        ]
        PlaySound(f"mono/card/{choice(glow)}", 0.7, position)