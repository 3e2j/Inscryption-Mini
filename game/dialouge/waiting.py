from engine.threadingEngine import threaded
from time import sleep
from __main__ import Developer_Mode
import unicurses

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
    if Developer_Mode:
        unicurses.mvaddstr(4, 0, f"Removed {WaitIdOrKey} from waitUntilKiller")

def sendWaitIdOrKey(WaitIdOrKey):
    waitUntilKiller.append(WaitIdOrKey)

def deleteKey(WaitIdOrKey):
    waitUntilKiller.remove(WaitIdOrKey)

#don't thread this, needs to wait like basic python, not be skipped through threading
def waitUntil(WaitIdOrKey, isKeyboardInput, *arguments, triangle=False):
    wU = True
    if Developer_Mode:
        unicurses.mvaddstr(3, 0, f"Listening for {WaitIdOrKey}, Keyboard: '{isKeyboardInput}'    ")
    from uuid import uuid4
    UUID = uuid4().hex
    while wU:
        if isKeyboardInput is not False:
            from engine.screenSetup import key
            if key in isKeyboardInput:
                wU = False
                UUID = False # Stops UUID of triangle
                if Developer_Mode:
                    unicurses.mvaddstr(3, 0, f"Completed Wait Key Loop for {WaitIdOrKey}    ")
                if not WaitIdOrKey == "leshyTalking":
                    waitUntilKiller.append(WaitIdOrKey)
                if not WaitIdOrKey == "leshyTalking":
                    deleteResidueKeys(WaitIdOrKey)
            else:
                if triangle:
                    from engine.screenSetup import brightorange, sw, sh
                    @threaded
                    def DisplayTriangle():
                        while not UUID == False:
                            unicurses.mvaddstr(sh // 2 -28, sw // 2, "▲", brightorange)
                            sleep(0.5)
                            if UUID == False:
                                break
                            unicurses.mvaddstr(sh // 2 -28, sw // 2, "▲", brightorange | unicurses.A_BOLD)
                            sleep(0.5)
                        unicurses.mvaddstr(sh // 2 -28, sw // 2, " ")
                    DisplayTriangle()
                    triangle = False

        else:
            if WaitIdOrKey in waitUntilKiller:  # Checks if waitID has been added to waitUntilKiller
                wU = False
                waitUntilKiller.remove(WaitIdOrKey)  # Removes key

                if Developer_Mode:
                    unicurses.mvaddstr(3, 0, f"Completed Wait Loop for {WaitIdOrKey}    ")
            sleep(0.25)  # waits 0.25s for preformance
            unicurses.refresh()
def waitTimerSecs(Seconds):
    while not Seconds == 0:
        sleep(1)
        if Developer_Mode:
            unicurses.mvaddstr(3, 0, f"waiting for {Seconds} seconds    ")
        unicurses.refresh()
        Seconds -= 1