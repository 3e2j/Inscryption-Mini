from unicurses import mvaddstr
from engine.screenSetup import sh,sw,white,gray,brightorange,red, ResetKey
from time import sleep
from __main__ import Developer_Mode


from game.card import \
    blankCardSpace, \
    bigblank, \
    lobster, \
    biglobster, \
    lobster2, \
    biglobster2, \
    squirrel, \
    bigsquirrel

from engine.soundEngine import PlaySound
import random

from array import *

BoardID = [
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#0
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#1
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"]#2
    ]
deck = [] # Users current deck of cards

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
    deck.append(["lobster2",lobster2[12],lobster2[13], lobster2[14]]) # type, attack, health, blood
    if Developer_Mode:
        #mvaddstr(22, 0, BoardID)
        mvaddstr(23,0,deck)

reference = {
        "blankCardSpace" : blankCardSpace,
        "bigblank" : bigblank,
        "lobster" : lobster,
        "biglobster" : biglobster,
        "lobster2": lobster2,
        "biglobster2": biglobster2,
        "squirrel" : squirrel,
        "bigsquirrel": bigsquirrel
    }

def PlaceCardOrColorChange(cardNum, row, deckCardInfo, placement = True, color = white): #Assumes cardNum is 1-4
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
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 9 - deckCardInfo[3], "δ" * deckCardInfo[3], color)  # Attack
    if placement:
        CardPlaySound("normal",(soundPosition, 0, 1))
        global BoardID
        BoardID[row][cardNum] = [CardType,deckCardInfo[1],deckCardInfo[2],deckCardInfo[3]]
        #mvaddstr(22,0,BoardID)

def printSideBig(deckCardInfo, color, blank=False):
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
        mvaddstr(sh // 2 + 15 + 28, sw // 2 + 90 - deckCardInfo[3], "δ" * deckCardInfo[3], color)

def positionPlacement(oldSelect=0):
    placementCount = 0
    sacrificeMade = False
    wU = True
    from game.dialouge.dialouge import clearLine
    while wU:
        ResetKey()
        posCenter = -30
        clearLine(21)
        PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
        if deck[oldSelect][3] > 0:
            mvaddstr(24,0,deck[oldSelect][3])
            PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, red)
        else:
            PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
        mvaddstr(sh // 2 + 21 ,sw // 2 + posCenter + (20 * placementCount),"^", brightorange)

        def changeOldCardToWhite():
            PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, white)

        checkInput = True
        SelectCardReturn = False
        while checkInput:
            from engine.screenSetup import key
            if not placementCount - 1 == -1:
                if key == "KEY_LEFT" or key == "a":
                    changeOldCardToWhite()
                    placementCount -= 1
                    checkInput = False
            if not placementCount + 1 == 4:
                if key == "KEY_RIGHT" or key == "d":
                    changeOldCardToWhite()
                    placementCount += 1
                    checkInput = False
            if key == "^[" or key == "x" and not sacrificeMade:
                changeOldCardToWhite()
                SelectCardReturn = True
                checkInput = False
                wU = False
            if key == "^J" or key == 'z':
                checkInput = False
                wU = False
    if SelectCardReturn:
        clearLine(21)
        SelectCardFromDeck(oldSelect)
    else:
        clearLine(21)
        PlaceCardOrColorChange(placementCount, 2, deck[oldSelect])
        deck.remove(deck[oldSelect])
        try:
            printSideBig(deck[0][0], gray)
        except:
            SelectCardFromDeck(0,True)
            printSideBig(None, None, True)

import unicurses

#First in the event of the players turn, allows a selection from their current deck.
def SelectCardFromDeck(count=0, turnOffArrows=False):
    if not turnOffArrows:
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
                if key == "^J" or key == 'z':
                    checkInput = False
                    wU = False
        printSideBig(deck[count], gray) # Gray's out the portrait to show selected
        positionPlacement(count) #Moves onto placement
    else:
        mvaddstr(sh // 2 + 2, sw // 2 + 55, " ")
        mvaddstr(sh // 2 + 2, sw // 2 + 99, " ")

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
        PlaySound(f"mono/card/{random.choice(normal)}", 0.7, position)
    if tone == "quick":
        quick = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{random.choice(quick)}", 0.7, position)
    if tone == "glow":
        glow = [
            "cardslot_glow#1",
            "cardslot_glow#2",
            "cardslot_glow#3",
            "cardslot_glow#4"
        ]
        PlaySound(f"mono/card/{random.choice(glow)}", 0.7, position)