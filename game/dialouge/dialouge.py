from time import sleep
import unicurses
from engine.screenSetup import sh, sw  # pointer to _curses.window object heap
from __main__ import Developer_Mode


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

    '''Important to note that all sleep times need to be within the actual refresh rate, IE: a multiple of 0.25'''


from engine.threading import threaded


@threaded
def deleteUnusedKeys(WaitIdOrKey):
    sleep(10)  # Give time for the functions to finish whatever they're doing
    exec(f"global {WaitIdOrKey} \ndel {WaitIdOrKey}")
    unicurses.mvaddstr(4, 0, f"Removed global {WaitIdOrKey}")


def waitUntil(WaitIdOrKey, isKeyboardInput, *arguments):
    wU = True
    if Developer_Mode:
        unicurses.mvaddstr(3, 0, f"Listening for {WaitIdOrKey}, Keyboard: '{isKeyboardInput}'    ")
    while wU == True:
        if isKeyboardInput is not False:  # No global decloration has to be declared for toggle
            try:
                key = unicurses.getkey()
                if key == isKeyboardInput:  # Enter
                    wU = False
                    if Developer_Mode:
                        unicurses.mvaddstr(3, 0, f"Completed Wait Key Loop for {WaitIdOrKey}    ")
                        exec(f"global {WaitIdOrKey} \n{WaitIdOrKey} = True")
                        deleteUnusedKeys(WaitIdOrKey)
                else:
                    unicurses.mvaddstr(11, 0, f"key ==== {key}                     ") # printing in bytes
            except:
                pass  # Avoids "none" error

        else:
            if WaitIdOrKey in globals():  # Checks if waitID has been added to globals(trigger)

                for x in arguments:  # Arguments
                    x
                wU = False

                if Developer_Mode:
                    unicurses.mvaddstr(3, 0, f"Completed Wait Loop for {WaitIdOrKey}    ")

                exec(
                    f"global {WaitIdOrKey} \ndel {WaitIdOrKey}")  # A sneaky bypass to delete WaitID without param/global errors

            sleep(0.25)  # waits 0.25s for preformance
            unicurses.refresh()


# Start Screen
def startScreen():
    # Two threads are required due to running simultaniously.
    @threaded
    def dialouge(status):
        if status == "init":
            centreFadeIn("Recommended to play in fullscreen for the best experience", -1, 0, 2)
        else:
            centreFadeOut("Recommended to play in fullscreen for the best experience", -1, 0, 2)

    @threaded
    def dialouge2(status):
        if status == "init":
            centreFadeIn("Press ENTER to confirm screen-size", 0, 0, 2)
            dancingMan(1, 0, 0.5)
            #exec("global DialougeSendIn \nDialougeSendIn = True")  # Quick line to push out a global value
        else:
            centreFadeOut("Press ENTER to confirm screen-size", 0, 0, 2)

    @threaded
    def dialouge3(status):
        if status == "init":
            centreFadeIn(" ┗(･o･ )┓ ", 1, 0, 2)
        else:
            centreFadeOut(" ┗(･o･ )┓ ", 1, 0, 2)
            exec("global DialougeSendOut \nDialougeSendOut = True")  # Quick line to push out a global value

    @threaded
    def dancingMan(heightChange, widthChange, TotalTime):
        while "DialougeSendIn" not in globals():
            centreDialougeX(" ┏(・o･)┛", heightChange, widthChange)
            sleep(TotalTime / 2)
            centreDialougeX(" ┗(･o･ )┓ ", heightChange, widthChange)
            sleep(TotalTime / 2)

    dialouge("init")
    dialouge2("init")
    dialouge3("init")
    waitUntil("DialougeSendIn", "KEY_RIGHT")
    #waitUntil("DialougeSendIn", False)
    dialouge("out")
    dialouge2("out")
    dialouge3("out")  # Assumes last thread therefore will have wait toggle (note: changes for time periods given)
    waitUntil("DialougeSendOut", False)
    # waitUntil("DialougeSendIn","\n")


def mainMenu():
    from time import sleep
    sleep(50)