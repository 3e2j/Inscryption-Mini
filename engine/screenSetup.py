from __main__ import Developer_Mode

black = None
dark_gray = None
gray = None
light_gray = None
white = None
magenta = None
red = None
orange = None
brightorange = None
mediocre_gray = None
dark_orange = None
yellow = None
purple = None

sh = None
sw = None

key = None

import time
from time import localtime, sleep

import unicurses
''' 
no, it's not a unicorn. But it is the terminal based framework that I'm runnning the program in.
Originally was coded in Curses, but switched to UniCurses to support Windows machines. 
'''

def CursesStartup(RunThroughFullGame):
    def main(s):
        global StandardScreen
        StandardScreen = unicurses.initscr()

        '''OLD resize code:
         couldn't get screen-manipulation to work.
         Had to settle for a simple F11 press by default.
         '''


        unicurses.clear()  # Clear the whole Screen
        #unicurses.timeout(100)  # Refresh rate
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
        unicurses.init_color(9,
                          0x35 * 1000 // 0xff,
                          0x35 * 1000 // 0xff,
                          0x35 * 1000 // 0xff)
        #Orange
        unicurses.init_color(5,
                          0xaa * 1000 // 0xff,
                          0x5b * 1000 // 0xff,
                          0x20 * 1000 // 0xff)
        #Brighter Orange
        unicurses.init_color(6,
                          0xad * 1000 // 0xff,
                          0x53 * 1000 // 0xff,
                          0x16 * 1000 // 0xff)
        # White
        unicurses.init_color(7, # for some reason default_colors sets the font to '7', which means I must make white ID 7.
                             0xe5 * 1000 // 0xff, # Note: Is not true white (FFFFFF) due to overpowering intense light
                             0xe5 * 1000 // 0xff,
                             0xe5 * 1000 // 0xff)
        #Red
        unicurses.init_color(8,
                             0xa0 * 1000 // 0xff,
                             0x00 * 1000 // 0xff,
                             0x00 * 1000 // 0xff)
        #Dark Orange
        unicurses.init_color(10,
                             0x82 * 1000 // 0xff,
                             0x3e * 1000 // 0xff,
                             0x10 * 1000 // 0xff)
        # Yellow
        unicurses.init_color(11,
                             0xad * 1000 // 0xff,
                             0x9e * 1000 // 0xff,
                             0x00 * 1000 // 0xff)
        # Purple
        unicurses.init_color(12,
                             0xb2 * 1000 // 0xff,
                             0x00 * 1000 // 0xff,
                             0xff * 1000 // 0xff)

        unicurses.init_pair(1, unicurses.COLOR_BLACK, -1)
        unicurses.init_pair(2, 2, -1)
        unicurses.init_pair(3, 3, -1)
        unicurses.init_pair(4, 4, -1)
        unicurses.init_pair(5, 7, -1)
        unicurses.init_pair(7, unicurses.COLOR_MAGENTA, -1)
        unicurses.init_pair(6, 8, -1)
        unicurses.init_pair(8, 5, -1)
        unicurses.init_pair(9, 6, -1)
        unicurses.init_pair(10, 9, -1)
        unicurses.init_pair(11, 10, -1)
        unicurses.init_pair(12, 11, -1)
        unicurses.init_pair(13, 12, -1)

        global black, dark_gray, gray, light_gray, white, red, magenta, orange, brightorange, mediocre_gray, dark_orange, yellow, purple
        black = unicurses.color_pair(1)
        dark_gray = unicurses.color_pair(2)
        gray = unicurses.color_pair(3)
        light_gray = unicurses.color_pair(4)
        white = unicurses.color_pair(5)
        red = unicurses.color_pair(6)
        magenta = unicurses.color_pair(7)
        orange = unicurses.color_pair(8)
        brightorange = unicurses.color_pair(9)
        mediocre_gray = unicurses.color_pair(10)
        dark_orange = unicurses.color_pair(11)
        yellow = unicurses.color_pair(12)
        purple = unicurses.color_pair(13)

        if Developer_Mode: #Dev subtitles
            unicurses.mvaddstr(0, 0, "Developer Stats", magenta)
            unicurses.mvaddstr(1, 0, "  Threading", magenta)
            unicurses.mvaddstr(6, 0, "Screen Height/Width", magenta)
            unicurses.mvaddstr(7, 0, f"{sh, sw}", white)
            unicurses.mvaddstr(8, 0, "Sound", magenta)
            unicurses.mvaddstr(11, 0, "Key-press", magenta)

        from engine.threadingEngine import threaded

        @threaded
        def RefreshTheScreenContantly():
            while True:
                unicurses.refresh()
                sleep(0.02)

        RefreshTheScreenContantly()

        unicurses.nodelay(StandardScreen, True)

        @threaded
        def GetCurrentKeyPress():
            global key
            while True:
                key = str(unicurses.getkey(), "utf-8")  # Grab input and Decode bytes
                #if Developer_Mode:
                #    unicurses.mvaddstr(12, 0, f"{key}             ") # Set nodelay to False

        GetCurrentKeyPress()

        if Developer_Mode:
            from threading import activeCount
            @threaded
            def ThreadingChecker():  # Checks active amount of threads
                from time import sleep
                while True:
                    try:
                        unicurses.mvaddstr(2, 0, f"Number of running threads: {activeCount()}       ")
                    except:
                        pass
                    sleep(2)
                return ThreadingChecker
            ThreadingChecker()
        if RunThroughFullGame:
            import game.cabin
        else: #Dev skip
            print("Skipping to certain section")
            import game.cabin
            #Add in whatever section here, IE: startScreen(), mainMenu(), etc...
        unicurses.endwin()
    return main

def ResetKey():
    global key
    key = None

@CursesStartup(RunThroughFullGame=True)
def StartCurses():
    pass

if Developer_Mode:
    print(f"Started Curses Terminal at {time.asctime(localtime())}")
StartCurses #RunThroughFullGame