from time import sleep
import unicurses
from engine.screenSetup import sh, sw  # pointer to _curses.window object heap
from __main__ import Developer_Mode


'''
Below is all dialouge usable functions that can be called upon to simplify
screen updates that are called constantly
'''


def screenClear():
    unicurses.clear()


from engine.screenSetup import dark_gray, gray, light_gray, white


# Instant Dialouge
def centreDialouge(x):
    unicurses.mvaddstr(sh // 2, sw // 2 - len(x) // 2, x)


# Extended varation of instant dialouge
def centreDialougeX(x, heightChange, widthChange):
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x)


# Typing Dialouge
def centreDialougeChar(x, TimeTaken):
    count = 0
    for char in x:
        unicurses.mvaddstr(sh // 2, sw // 2 - len(x) // 2 + count, char)
        count += 1
        sleep(TimeTaken)


# Typing Dialouge Extened
def centreDialougeCharX(x, TimeTaken, heightChange, widthChange):
    count = 0
    for char in x:
        unicurses.mvaddstr((sh // 2) + heightChange, sw // 2 - len(x) // 2 + widthChange + count, char)
        count += 1
        sleep(TimeTaken)


# Fade In
def centreFadeIn(x, heightChange, widthChange, TotalTime):
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, dark_gray)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, gray)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, light_gray)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, white)


# Fade Out
def centreFadeOut(x, heightChange, widthChange, TotalTime):
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, white)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, light_gray)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, gray)
    sleep(TotalTime / 4)
    unicurses.mvaddstr(sh // 2 + heightChange, sw // 2 - len(x) // 2 + widthChange, x, dark_gray)

def clearLine(heightChange):
    y = 0
    x = 0
    unicurses.move(sh // 2 + heightChange, 0)
    unicurses.clrtoeol()
    unicurses.move(y, x)