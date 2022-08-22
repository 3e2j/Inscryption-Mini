import random

import unicurses

from engine.screenSetup import sh, sw, white, orange, brightorange
from time import sleep
from engine.threadingEngine import threaded
from unicurses import  mvaddstr, refresh, napms
from random import randint

eyesStatus = [] #Open, Closed, Talking, Opening, Stop (kills eyes)

eyeDraw = [
" ████            ████ ", #0
"██  ██          ██  ██", #1
" ████            ████ ", #2
"                            ", #3
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
    NormalOffset = eyeDraw[2]
    ExtendedOffset = eyeDraw[3]
    eyepos = -25
    while "Stop" not in eyesStatus:
        while "Open" in eyesStatus:
            refresh()
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[0],white) #Top
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[1],white) # Mid
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[2], white) # Bottom
            randomTime = randint(8,10)
            counter = 0
            while "Open" in eyesStatus and not counter*4 == randomTime:
                napms(250)
                counter += 1
            if "Open" in eyesStatus:
                #blinking
                mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(ExtendedOffset) // 2), eyeDraw[3],white) #Top blank
                napms(100) and refresh()
                mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(ExtendedOffset) // 2), eyeDraw[3],white) # Mid blank
                napms(100) and refresh()
                mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(ExtendedOffset) // 2), eyeDraw[3], white) # Bottom blank
                napms(120) and refresh()
                mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[2], white)  # Bottom
                napms(100) and refresh()
                mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[1], white)  # Mid
            y=0
        while "Opening" in eyesStatus:
            napms(2500) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[4], white)  # Bottom
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[5], white)  # Mid
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[0], white)  # Top
            napms(2000) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[2], white)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[1], white)  # Mid
            napms(2000) and refresh()
            SetEyes("Open")
        while "Talking" in eyesStatus:
            mvaddstr(15, 0, f"Talking")
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[6], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[7], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[8], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[9], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[10], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[11], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[12], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[13], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[14], orange)  # Top
            napms(220) and refresh()
            mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[15], orange)  # Bottom
            mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[16], orange)  # Mid
            mvaddstr(sh // 2 + eyepos, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[17], orange)  # Top
            napms(220) and refresh()


            
    eyesStatus.remove("Stop")

def SetEyes(eyeMode):
    global eyesStatus
    eyesStatus.append(eyeMode) #Add new mode
    if not eyesStatus[0] == eyeMode:
        eyesStatus.pop(0) # remove old mode
# Tone can be either -  calm, curious, or frustrated
def leshyTalk(speech, tone="calm", volume=0.4, position=(0,0,0)):
    from engine.soundEngine import PlaySound
    mvaddstr(sh // 2 -27, sw // 2 - len(speech) // 2, speech.upper(), brightorange)
    SetEyes("Talking")
    if tone == "calm":
        calm = [
            "voice_calm#1",
            "voice_calm#2",
            "voice_calm#3",
            "voice_calm#4",
            "voice_calm#5",
            "voice_calm#6",
            "voice_calm#7",
            "voice_calm#8",
            "voice_calm#9",
            "voice_calm#10",
            "voice_calm#11",
            "voice_calm#12"
        ]
        PlaySound(f"stereo/leshy/{random.choice(calm)}", volume, position)
    if tone == "curious":
        curious = [
            "voice_curious#1",
            "voice_curious#2",
            "voice_curious#3",
            "voice_curious#4",
            "voice_curious#5",
            "voice_curious#6",
            "voice_curious#7",
            "voice_curious#8",
            "voice_curious#9",
            "voice_curious#10",
            "voice_curious#11"
        ]
        PlaySound(random.choice(curious), volume, position)
    if tone == "frustrated":
        frustrated = [
            "voice_frustrated#1",
            "voice_frustrated#2",
            "voice_frustrated#3",
            "voice_frustrated#4",
            "voice_frustrated#5",
            "voice_frustrated#6",
            "voice_frustrated#7",
            "voice_frustrated#8"
        ]
        PlaySound(random.choice(frustrated), volume, position)