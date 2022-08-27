from unicurses import mvaddstr
from engine.screenSetup import sh,sw,white,gray,brightorange, ResetKey
from time import sleep
from __main__ import Developer_Mode


from game.card import blankCardSpace, lobster, biglobster, lobster2, biglobster2

from engine.soundEngine import PlaySound
import random

from array import *

BoardID = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
] # 0 represents 'blank'
deck = [] # Users current deck of cards

def startBoard():
    cardCentringOriginal = -38
    soundPositionOriginal = -0.2
    cardHeight = -15
    for cardRow in range(0,3):
        cardCentering = cardCentringOriginal
        soundPosition = soundPositionOriginal
        for card in range(0,4):
            mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, blankCardSpace[0])
            heightAddition = 1
            for line in range(0,10):
                mvaddstr(sh // 2 + cardHeight + heightAddition, sw // 2 + cardCentering, blankCardSpace[1])
                heightAddition += 1
            heightAddition = 0
            mvaddstr(sh // 2 + cardHeight +11, sw // 2 + cardCentering, blankCardSpace[11])
            cardCentering += 20
            CardPlaySound("glow",(soundPosition, 0,1))
            soundPosition += 0.1
            sleep(0.2)
        cardHeight += 12
    global BoardID
    BoardID = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    deck.append(["lobster",lobster[12],lobster[13]]) # type, attack, health
    deck.append(["lobster2", lobster2[12], lobster2[13]])  # type, attack, health
    if Developer_Mode:
        mvaddstr(22, 0, BoardID)
        mvaddstr(23,0,deck)

type = {
        "blankCardSpace" : blankCardSpace,
        "lobster" : lobster,
        "biglobster" : biglobster,
        "lobster2": lobster2,
        "biglobster2": biglobster2
    }

def PlaceCard(cardNum, row, CardType): #Assumes cardNum is 1-4
    cardCentering = -38 + (20 * cardNum) #Centering; changes 1-4 to 0-3
    soundPosition = -0.2
    cardHeight = -15 + (12 * row) #Height; changes 1-3 to 0-2
    mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, type[CardType][0]) # Drawing out the card
    mvaddstr(sh // 2 + cardHeight + 1, sw // 2 + cardCentering, type[CardType][1])
    mvaddstr(sh // 2 + cardHeight + 2, sw // 2 + cardCentering, type[CardType][2])
    mvaddstr(sh // 2 + cardHeight + 3, sw // 2 + cardCentering, type[CardType][3])
    mvaddstr(sh // 2 + cardHeight + 4, sw // 2 + cardCentering, type[CardType][4])
    mvaddstr(sh // 2 + cardHeight + 5, sw // 2 + cardCentering, type[CardType][5])
    mvaddstr(sh // 2 + cardHeight + 6, sw // 2 + cardCentering, type[CardType][6])
    mvaddstr(sh // 2 + cardHeight + 7, sw // 2 + cardCentering, type[CardType][7])
    mvaddstr(sh // 2 + cardHeight + 8, sw // 2 + cardCentering, type[CardType][8])
    mvaddstr(sh // 2 + cardHeight + 9, sw // 2 + cardCentering, type[CardType][9])
    mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering, type[CardType][10])
    mvaddstr(sh // 2 + cardHeight + 11, sw // 2 + cardCentering, type[CardType][11])

    mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 2, f"{type[CardType][12]}†") # Attack
    mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 13, f"{type[CardType][13]}♥")  # Attack
    CardPlaySound("normal",(soundPosition, 0, 1))
    global BoardID
    BoardID[row - 1][cardNum - 1] = [CardType,type[CardType][12],type[CardType][13]]
    mvaddstr(22,0,BoardID)
    printSideBig(CardType, white)

def printSideBig(CardType, color):
    count = 0
    portrait = f"big{CardType}"
    for x in range(0,31):
        mvaddstr(sh // 2 -12 + count, sw // 2 + 58, type[portrait][count], color)
        count +=1
    mvaddstr(sh // 2 - 12 + 28, sw // 2 + 64, f"{type[CardType][12]}†", color)
    mvaddstr(sh // 2 - 12 + 28, sw // 2 + 90, f"{type[CardType][13]}♥", color)

def positionPlacement(CardType, oldSelect=0):
    placementCount = 0
    wU = True
    while wU:
        ResetKey()
        posCenter = -30
        from game.dialouge.dialouge import clearLine
        clearLine(21)
        mvaddstr(sh // 2 + 21 ,sw // 2 + posCenter + (20 * placementCount),"^", brightorange)

        checkInput = True
        SelectCardReturn = False
        while checkInput:
            from engine.screenSetup import key
            if not placementCount - 1 == -1:
                if key == "KEY_LEFT" or key == "a":
                    placementCount -= 1
                    checkInput = False
            # elif key == "KEY_LEFT" or key == "a":
            #     from game.dialouge.leshy import leshyTalk
            #     leshyTalk("You cannot go further then the board")
            if not placementCount + 1 == 4:
                if key == "KEY_RIGHT" or key == "d":
                    placementCount += 1
                    checkInput = False
            if key == "^[":
                SelectCardReturn = True
                checkInput = False
                wU = False
            if key == "^J" or key == 'z':
                checkInput = False
                wU = False
    if SelectCardReturn:
        SelectCardFromDeck(oldSelect)
    else:
        PlaceCard(placementCount, 2, CardType)

import unicurses

def SelectCardFromDeck(count=0):
    wU = True
    while wU:
        ResetKey()
        canGoLeft = False
        canGoRight = False
        printSideBig(deck[count][0], white)
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
            from engine.screenSetup import key
            if canGoLeft:
                if key == "KEY_LEFT" or key == "a":
                    count -= 1
                    checkInput = False
            if canGoRight:
                if key == "KEY_RIGHT" or key == "d":
                    count += 1
                    checkInput = False
            if key == "^J" or key == 'z':
                checkInput = False
                wU = False
        mvaddstr(31,0,count)
    printSideBig(deck[count][0], gray)
    positionPlacement(deck[count][0],count)
    pass

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