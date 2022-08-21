from __main__ import Developer_Mode

black = None
dark_gray = None
gray = None
light_gray = None
white = None
magenta = None
red = None

sh = None
sw = None

import time
from time import localtime, sleep

import unicurses
''' 
no, it's not a unicorn. But it is the terminal based framework that I'm runnning the program in.
Originally was coded in Curses, but switched to UniCurses to support windows machines. 
'''

def PrefixReimportCurses(ConfirmResolution):
    def main(s):
        #global StandardScreen  # Globalising Standard Screen to not require import to every file that wants screen updates
        StandardScreen = unicurses.initscr()


        #unicurses.resize_term(*unicurses.getmaxyx(StandardScreen))
        #unicurses.wresize(StandardScreen,*unicurses.getmaxyx(StandardScreen))
        #unicurses.clear()
        #unicurses.refresh()

        '''OLD resize code:
         couldn't get screen-manipulation to work.
         Had to settle for a simple F11 press by default.
         '''


        unicurses.clear()  # Clear the whole Screen
        unicurses.timeout(250)  # Refresh rate
        unicurses.curs_set(0)
        unicurses.start_color()
        unicurses.use_default_colors()  # Makes the terminal the original color
        unicurses.keypad(StandardScreen, True);

        global sh, sw
        sh, sw = unicurses.getmaxyx(StandardScreen)

        # Color Init (not using background colors)
        # gray's from black to white
        unicurses.init_color(2,
                          0x1b * 1000 // 0xff,
                          0x1b * 1000 // 0xff,
                          0x1b * 1000 // 0xff)
        unicurses.init_color(3,
                          0x6f * 1000 // 0xff,
                          0x6f * 1000 // 0xff,
                          0x6f * 1000 // 0xff)
        unicurses.init_color(4,
                          0x9d * 1000 // 0xff,
                          0x9d * 1000 // 0xff,
                          0x9d * 1000 // 0xff)

        unicurses.init_pair(1, unicurses.COLOR_BLACK, -1)
        unicurses.init_pair(2, 2, -1)
        unicurses.init_pair(3, 3, -1)
        unicurses.init_pair(4, 4, -1)
        unicurses.init_pair(5, unicurses.COLOR_WHITE, -1)
        unicurses.init_pair(6, unicurses.COLOR_RED, -1)
        unicurses.init_pair(7, unicurses.COLOR_MAGENTA, -1)

        global black, dark_gray, gray, light_gray, white, red, magenta
        black = unicurses.color_pair(1)
        dark_gray = unicurses.color_pair(2)
        gray = unicurses.color_pair(3)
        light_gray = unicurses.color_pair(4)
        white = unicurses.color_pair(5)
        red = unicurses.color_pair(6)
        magenta = unicurses.color_pair(7)

        if Developer_Mode:
            unicurses.mvaddstr(0, 0, "Developer Stats", red)
            unicurses.mvaddstr(1, 0, "  Threading", magenta)
            unicurses.mvaddstr(6, 0, "Screen Height/Width", magenta)
            unicurses.mvaddstr(7, 0, f"{sh, sw}")

        from engine.threadingEngine import threaded
        from threading import activeCount
        @threaded
        def ThreadingChecker():
            from time import sleep
            while True:
                try:
                    unicurses.mvaddstr(5, 0, f"Number of running threads: {activeCount()}")
                except:
                    pass
                sleep(2)
            return ThreadingChecker

        from game.dialouge.dialouge import startScreen, mainMenu
        if ConfirmResolution:
            if Developer_Mode:
                ThreadingChecker()
            startScreen()
        else:
            print("RAN THROUGH MAIN MENU")
            unicurses.mvaddstr(7, 0, f"Tried to call MainMenu {sh, sw}")
            unicurses.refresh()
            sleep(500)
            #mainMenu() #This will go to the main menu but i'm skipping it to develop the game
        unicurses.endwin()
    print("RAN THROUGH SCRIPT")
    return main


@PrefixReimportCurses
def ReimportCurses(ConfirmResolution):
    pass

if Developer_Mode:
    print(f"startScreen at {time.asctime(localtime())}")
ReimportCurses(True)

# Restarting the VM
if Developer_Mode:
    print(f"mainMenu at {time.asctime(localtime())}")
#reimportCursesModule(False)