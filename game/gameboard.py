from unicurses import mvaddstr
from engine.screenSetup import sh,sw
from time import sleep


from game.card import blankCardSpace, lobster

from engine.soundEngine import PlaySound
import random

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
            sleep(0.05)
        cardHeight += 12



def PlaceCard(cardNum, row, CardType): #Assumes cardNum is 1-4
    cardCentering = -38 + (20 * (cardNum-1)) #Centering; changes 1-4 to 0-3
    soundPosition = -0.2
    cardHeight = -15 + (12 * (row -1)) #Height; changes 1-3 to 0-2
    type = {
        "blankCardSpace" : blankCardSpace,
        "lobster" : lobster
    }
    mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, type[CardType][0])
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
    CardPlaySound("normal",(soundPosition, 0, 1))




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
        PlaySound(f"mono/card/{random.choice(normal)}", 0.5, position)
    if tone == "quick":
        quick = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{random.choice(quick)}", 0.5, position)
    if tone == "glow":
        glow = [
            "cardslot_glow#1",
            "cardslot_glow#2",
            "cardslot_glow#3",
            "cardslot_glow#4"
        ]
        PlaySound(f"mono/card/{random.choice(glow)}", 0.5, position)