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
    import uuid
    UUID = uuid.uuid4().hex
    unicurses.mvaddstr(26, 0, UUID)
    while wU == True:
        if isKeyboardInput is not False:
            from engine.screenSetup import key
            if key == isKeyboardInput or key == [item for item in arguments if item[0]]:  # Enter
                wU = False
                if Developer_Mode:
                    unicurses.mvaddstr(3, 0, f"Completed Wait Key Loop for {WaitIdOrKey}    ")
                waitUntilKiller.append(WaitIdOrKey)
                UUID = False
                if WaitIdOrKey == "leshyTalking":
                    deleteKey("leshyTalking")
                else:
                    deleteResidueKeys(WaitIdOrKey)
            else:
                if triangle:
                    from engine.screenSetup import brightorange, sw, sh
                    from game.dialouge.leshy import eyepos
                    @threaded
                    def DisplayTriangle():
                        while not UUID == False:
                            unicurses.mvaddstr(sh // 2 + eyepos - 3, sw // 2, "▲", brightorange)
                            sleep(0.5)
                            if UUID == False:
                                break
                            unicurses.mvaddstr(sh // 2 + eyepos - 3, sw // 2, "▲", brightorange | unicurses.A_BOLD)
                            sleep(0.5)
                        unicurses.move(sh // 2 + eyepos - 3, 0)  # Triangle
                        unicurses.clrtoeol()
                        unicurses.move(y, x)
                    DisplayTriangle()
                    triangle = False

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
    while not Seconds == 0:
        for x in range(0, 4):
            sleep(0.25)
            if Developer_Mode:
                unicurses.mvaddstr(3, 0, f"waiting for {Seconds} seconds    ")
            unicurses.refresh()
        Seconds -= 1