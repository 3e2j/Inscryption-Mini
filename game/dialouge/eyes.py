from engine.screenSetup import sh, sw, white, black, orange
from time import sleep
from engine.threadingEngine import threaded
from unicurses import  mvaddstr, refresh, napms
from random import randint

eyesStatus = [] #Open, Closed, Talking, Opening, Stop (kills eyes)

eyeDraw = [
" ████            ████ ", #0
"██  ██          ██  ██", #1
" ████            ████ ", #2
"                      ",
" █  █            █  █ ", #4
"██████          ██████", #5

"  ███            ███  ", #6
"██ █              █ ██", #7  #Eye Roll 1
"  █ █            █ █  ", #8

" ███              ███ ", #9
"  █ ██          ██ █  ", #10  #Eye Roll 2
" █ █              █ █ ", #11

" █ █              █ █ ", #12
"  █ ██          ██ █  ", #13  #Eye Roll 3
" ███              ███ ", #14

"  █ █            █ █  ", #15
"██ █              █ ██", #16  #Eye Roll 4
"  ███            ███  ", #17

]

@threaded
def StartEyes():
    x = eyeDraw[0]
    eyepos = -20
    while "Stop" not in eyesStatus:
        while "Open" in eyesStatus:
            refresh()
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[0],white) #Top
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[1],white) # Mid
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[2], white) # Bottom
            sleep(randint(8,10))
            #blinking
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[3],white) #Top blank
            napms(100) and refresh()
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[3],white) # Mid blank
            napms(100) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[3], white) # Bottom blank
            napms(120) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[2], white)  # Bottom
            napms(100) and refresh()
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[1], white)  # Mid
        while "Opening" in eyesStatus:
            napms(2500) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[4], white)  # Bottom
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[5], white)  # Mid
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[0], white)  # Top
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[2], white)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[1], white)  # Mid
            napms(2000) and refresh()
            SetEyes("Open")
        while "Talking" in eyesStatus:
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[6], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[7], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[8], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[9], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[10], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[11], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[12], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[13], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[14], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(x) // 2), eyeDraw[15], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(x) // 2), eyeDraw[16], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(x) // 2), eyeDraw[17], orange)  # Top
            napms(220) and refresh()


            
    eyesStatus.remove("Stop")

def SetEyes(eyeMode):
    global eyesStatus
    eyesStatus.append(eyeMode) #Add new mode
    if not eyesStatus[0] == eyeMode:
        eyesStatus.pop(0) # remove old mode