import random

firstGame = True

characterPosition = "| A |"
characterPlacementPiece = "| X |"
blank = "|   |"

# Auto Placement for the character at [1,1] coords
characterX = 1
characterY = 1


def powerCard():
    '''Power Card definition, will auto assign random numbers to be drawn'''
    powerLevel = random.randint(1, 5)
    healthLevel = random.randint(1, 6)
    # sigil
    if firstGame == False:
        sacrifice = random.choice(["bone", "health"], weights=[10, 30])
    else:
        sacrifice = "health"


# Initialise the Board

# Setup the blank board
board = [[blank for a in range(4)] for b in range(3)]

# The reference board of correctly PLACED peices (default none)
boardActual = []
boardActual = board

# Initalise the Player 'Placement Mode' Postion
board[characterY][characterX] = characterPosition

import os  # TEST FOR SLEEP WILL PORT DIALOGUE TO DIALOUGE
from time import sleep  # SAME

import curses

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Thread the input to allow for
from threading import Thread

key = curses.KEY_DOWN


def inputamundo():
    while MT_S_inputamundo:
        next_key = w.getch()
        global key
        key = key if next_key == -1 else next_key

        if key == curses.KEY_DOWN:
            print("down")
        elif key == curses.KEY_UP:
            print("up")
        elif key == curses.KEY_RIGHT:
            print("right")
        elif key == curses.KEY_LEFT:
            print("left")
    pass


inputThread = Thread(target=inputamundo)

eyesClosed = False

while firstGame == True:
    global MT_S_inputamundo
    MT_S_inputamundo = True
    os.system("clear")
    inputThread.start()
    if eyesClosed == True:
        print("-   -")
        sleep(0.5)
        eyesClosed = False
    else:
        print("O   O")
        sleep(3)
        eyesClosed = True
    print("Input:")
    MT_S_inputamundo = False
    inputThread.join()