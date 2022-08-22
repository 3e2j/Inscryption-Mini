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


from engine.threadingEngine import threaded

'''
Below is code used as a waiting timer, this will allow any function to wait until a requirement is met.
This could be simplified to a simple:

while WaitIDOrKey not in waitUntilkiller

But I needed this to be dynamic to listen for other inputs (IE: keypad inputs)
'''

waitUntilKiller = []

@threaded
def deleteResidueKeys(WaitIdOrKey):
    sleep(10)  # Give time for the functions to finish whatever they're doing
    try:
        waitUntilKiller.remove(WaitIdOrKey)
    except:
        pass
    unicurses.mvaddstr(4, 0, f"Removed {WaitIdOrKey} from waitUntilKiller")

def sendWaitIdOrKey(WaitIdOrKey):
    waitUntilKiller.append(WaitIdOrKey)

def deleteKey(WaitIdOrKey):
    waitUntilKiller.remove(WaitIdOrKey)


#don't thread this, needs to wait like basic python, not be skipped through threading
def waitUntil(WaitIdOrKey, isKeyboardInput, *arguments):
    wU = True
    if Developer_Mode:
        unicurses.mvaddstr(3, 0, f"Listening for {WaitIdOrKey}, Keyboard: '{isKeyboardInput}'    ")
    while wU == True:
        if isKeyboardInput is not False:
            try:
                key = str(unicurses.getkey(),"utf-8") #Grab input and Decode bytes
                if key == isKeyboardInput or [item for item in arguments if item[0] == key]:  # Enter
                    wU = False
                    if Developer_Mode:
                        unicurses.mvaddstr(3, 0, f"Completed Wait Key Loop for {WaitIdOrKey}    ")
                    waitUntilKiller.append(WaitIdOrKey)
                    deleteResidueKeys(WaitIdOrKey)
                    unicurses.flushinp()
                else:
                    if Developer_Mode:
                        unicurses.mvaddstr(11, 0, f"key ==== {key}                     ") # printing in bytes
            except:
                pass  # Avoids "none" error

        else:
            if WaitIdOrKey in waitUntilKiller:  # Checks if waitID has been added to waitUntilKiller

                # for x in arguments:  # Arguments
                #     x
                wU = False
                waitUntilKiller.remove(WaitIdOrKey)  # Removes key

                if Developer_Mode:
                    unicurses.mvaddstr(3, 0, f"Completed Wait Loop for {WaitIdOrKey}    ")
            sleep(0.25)  # waits 0.25s for preformance
            unicurses.refresh()
def waitTimerSecs(Seconds):
    if Developer_Mode:
        unicurses.mvaddstr(15, 0, f"waiting for {Seconds} seconds    ")
        unicurses.refresh()
    while not Seconds == 0:
        for x in range(1, 4):
            sleep(0.25)
            unicurses.mvaddstr(16, 0, f"waiting for {Seconds} seconds    ")
            unicurses.refresh()
        Seconds -= 1
