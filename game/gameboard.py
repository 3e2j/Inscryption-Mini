from unicurses import mvaddstr
from engine.screenSetup import sh,sw
from time import sleep


from game.card import blankCardSpace, test
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
            mvaddstr(sh // 2 + cardHeight, sw // 2 + cardCentering, test[0])
            mvaddstr(sh // 2 + cardHeight +1, sw // 2 + cardCentering, test[1])
            mvaddstr(sh // 2 + cardHeight +2, sw // 2 + cardCentering, test[2])
            mvaddstr(sh // 2 + cardHeight +3, sw // 2 + cardCentering, test[3])
            mvaddstr(sh // 2 + cardHeight +4, sw // 2 + cardCentering, test[4])
            mvaddstr(sh // 2 + cardHeight +5, sw // 2 + cardCentering, test[5])
            mvaddstr(sh // 2 + cardHeight +6, sw // 2 + cardCentering, test[6])
            mvaddstr(sh // 2 + cardHeight +7, sw // 2 + cardCentering, test[7])
            mvaddstr(sh // 2 + cardHeight +8, sw // 2 + cardCentering, test[8])
            mvaddstr(sh // 2 + cardHeight +9, sw // 2 + cardCentering, test[9])
            mvaddstr(sh // 2 + cardHeight +10, sw // 2 + cardCentering, test[10])
            mvaddstr(sh // 2 + cardHeight +11, sw // 2 + cardCentering, test[11])
            cardCentering += 20
            CardPlaySound("quick",(soundPosition, 0,1))
            soundPosition += 0.1
            sleep(0.3)
        cardHeight += 12

        


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
        normal = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{random.choice(normal)}", 0.5, position)