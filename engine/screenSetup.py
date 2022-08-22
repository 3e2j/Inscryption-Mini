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
Originally was coded in Curses, but switched to UniCurses to support Windows machines. 
'''

def CursesStartup(RunThroughFullGame):
    def main(s):

        StandardScreen = unicurses.initscr()

        '''OLD resize code:
         couldn't get screen-manipulation to work.
         Had to settle for a simple F11 press by default.
         '''


        unicurses.clear()  # Clear the whole Screen
        #unicurses.timeout(100)  # Refresh rate
        unicurses.nodelay(StandardScreen, True)
        unicurses.start_color() # init color
        unicurses.use_default_colors()  # Makes the terminal the original color
        unicurses.keypad(StandardScreen, True); #Makes arrow-keys work
        unicurses.noecho() #removes any keyboard-inputs typing letters like a terminal
        unicurses.curs_set(False) #removes the mouse

        global sh, sw
        sh, sw = unicurses.getmaxyx(StandardScreen) #Screen height/width

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
        #Orange
        unicurses.init_color(5,
                          0xaa * 1000 // 0xff,
                          0x5b * 1000 // 0xff,
                          0x20 * 1000 // 0xff)

        unicurses.init_pair(1, unicurses.COLOR_BLACK, -1)
        unicurses.init_pair(2, 2, -1)
        unicurses.init_pair(3, 3, -1)
        unicurses.init_pair(4, 4, -1)
        unicurses.init_pair(5, unicurses.COLOR_WHITE, -1)
        unicurses.init_pair(6, unicurses.COLOR_RED, -1)
        unicurses.init_pair(7, unicurses.COLOR_MAGENTA, -1)
        unicurses.init_pair(8, 5, -1)

        global black, dark_gray, gray, light_gray, white, red, magenta, orange
        black = unicurses.color_pair(1)
        dark_gray = unicurses.color_pair(2)
        gray = unicurses.color_pair(3)
        light_gray = unicurses.color_pair(4)
        white = unicurses.color_pair(5)
        red = unicurses.color_pair(6)
        magenta = unicurses.color_pair(7)
        orange = unicurses.color_pair(8)

        if Developer_Mode: #Dev subtitles
            unicurses.mvaddstr(0, 0, "Developer Stats", red)
            unicurses.mvaddstr(1, 0, "  Threading", magenta)
            unicurses.mvaddstr(6, 0, "Screen Height/Width", magenta)
            unicurses.mvaddstr(7, 0, f"{sh, sw}")
            unicurses.mvaddstr(8, 0, "Sound", magenta)

        from engine.threadingEngine import threaded
        from threading import activeCount
        @threaded
        def ThreadingChecker(): #Checks active amount of threads
            from time import sleep
            while True:
                try:
                    unicurses.mvaddstr(5, 0, f"Number of running threads: {activeCount()}")
                except:
                    pass
                sleep(2)
            return ThreadingChecker

        if RunThroughFullGame:
            if Developer_Mode:
                ThreadingChecker()
            import game.startScreen
        else: #Dev skip
            print("Skipping to certain section")
            import game.cabin
            #Add in whatever section here, IE: startScreen(), mainMenu(), etc...
        unicurses.endwin()
    return main

@CursesStartup(RunThroughFullGame=False)
def StartCurses():
    pass

if Developer_Mode:
    print(f"Started Curses Terminal at {time.asctime(localtime())}")
StartCurses #RunThroughFullGame