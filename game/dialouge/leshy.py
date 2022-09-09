import random

import unicurses

from engine.screenSetup import sh, sw, white, orange, brightorange, mediocre_gray, gray, dark_gray
from time import sleep
from engine.threadingEngine import threaded
from unicurses import  mvaddstr, refresh, napms
from random import randint
from game.dialouge.waiting import waitUntil, waitTimerSecs
from game.dialouge.dialouge import clearLine, screenClear

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

teethDraw = [
"██                                     ██",
"████                                 ████",
"  ██ █████ █████ ████ ████ ████ ████ ██  ",
"   █ █████ █████ ████ ████ ████ ████ █   "
]

handDraw = [
'      █      █  ', #0
'█     ██    ██  ',
'█     ██    █   ',
'█     ██   ██   ',
'██    ██   ██   ',
' ██   ██   █    ',
' ██   ██  ██    ',
' ██   ██  ██    ',
'  █   ██  ██    ',
'  ██████████    ',
'  ██████████   █',
'  ██████████   █',
'  ██████████   █',
'   █████████  ██',
'   ████████████ ',
'    ██████████  ',
'    ███████     ', #16
]
handDraw2 = [
'  █      █      ', #0
'  ██    ██     █',
'   █    ██     █',
'   ██   ██     █',
'   ██   ██    ██',
'    █   ██   ██ ',
'    ██  ██   ██ ',
'    ██  ██   ██ ',
'    ██  ██   █  ',
'    ██████████  ',
'█   ██████████  ',
'█   ██████████  ',
'█   ██████████  ',
'██  █████████   ',
' ████████████   ',
'  ██████████    ',
'     ███████    ' #16
]

finLDraw = [

]

finRDraw = [

]

eyepos = -25
@threaded
def StartEyes():
    NormalOffset = eyeDraw[2]
    TeethOffset = teethDraw[0]
    ExtendedOffset = eyeDraw[3]
    while "Stop" not in eyesStatus:
        while "Open" in eyesStatus:
            refresh()
            [mvaddstr(sh // 2 + eyepos + x, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[x],white) for x in range (0,3)] #Eyes
            randomTime = randint(8,10)
            counter = 0
            while "Open" in eyesStatus and not counter//4 >= randomTime:
                napms(250)
                counter += 1
            if "Open" in eyesStatus:
                #blinking
                clearLine(eyepos)
                napms(40) and refresh()
                clearLine(eyepos+1)
                napms(40) and refresh()
                clearLine(eyepos+2)
                napms(60) and refresh()
                mvaddstr(sh // 2 + eyepos+2, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[2], white)  # Bottom
                napms(40) and refresh()
                mvaddstr(sh // 2 + eyepos+1, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[1], white)  # Mid
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
            napms(2400) and refresh()
            SetEyes("Open")
        while "Talking" in eyesStatus:
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
        while "End" in eyesStatus:
            from engine.soundEngine import PlaySound
            PlaySound("stereo/leshy/giant_arm_descending", 0.7)
            [mvaddstr(sh // 2 + eyepos + x, (sw // 2) - (len(NormalOffset) // 2), eyeDraw[x], white) for x in range(0, 3)]
            mvaddstr(sh // 2 + eyepos + 6, (sw // 2) - (len(TeethOffset) // 2), teethDraw[3], white) # Teeth
            napms(170) and refresh()
            mvaddstr(sh // 2 + eyepos + 5, (sw // 2) - (len(TeethOffset) // 2), teethDraw[2], white)
            napms(170) and refresh()
            mvaddstr(sh // 2 + eyepos + 4, (sw // 2) - (len(TeethOffset) // 2), teethDraw[1], white)
            napms(170) and refresh()
            mvaddstr(sh // 2 + eyepos + 3, (sw // 2) - (len(TeethOffset) // 2), teethDraw[0], white)
            napms(170) and refresh()
            [mvaddstr(sh // 2 + eyepos -2 + x, (sw // 2) - 30 - len(handDraw[0]), handDraw[x], dark_gray) for x in range(0, 17)]
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) + 30, handDraw2[x], dark_gray) for x in range(0, 17)]
            sleep(0.8)
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) - 30 - len(handDraw[0]), handDraw[x], mediocre_gray) for x in range(0, 17)]
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) + 30, handDraw2[x], mediocre_gray) for x in range(0, 17)]
            sleep(0.8)
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) - 30 - len(handDraw[0]), handDraw[x], gray) for x in range(0, 17)]
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) + 30, handDraw2[x], gray) for x in range(0, 17)]
            sleep(0.8)
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) - 30 - len(handDraw[0]), handDraw[x], white) for x in range(0, 17)]
            [mvaddstr(sh // 2 + eyepos - 2 + x, (sw // 2) + 30, handDraw2[x], white) for x in range(0, 17)]
            sleep(0.8)
            screenClear()
            SetEyes("None")
            PlaySound("mono/candle/candle_loseLife")
        unicurses.refresh()



    eyesStatus.remove("Stop")

def SetEyes(eyeMode):
    global eyesStatus
    eyesStatus.append(eyeMode) #Add new mode
    try:
        if eyesStatus[1]:
            eyesStatus.pop(0) # remove old mode
    except:
        pass

# Tone can be either -  calm, curious, or frustrated
def leshyTalk(speech, tone="calm", skippable=False, volume=0.3, position=(0,0,0), overrideSetEyes = False):
    from engine.soundEngine import leshySound
    clearLine(-27)
    #talk

    mvaddstr(sh // 2 + eyepos -2, sw // 2 - len(speech) // 2, speech.upper(), brightorange)
    if overrideSetEyes:
        SetEyes(overrideSetEyes)
    else:
        SetEyes("Talking")
    #voice
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
        leshySound('calm', volume, position)
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
        leshySound('curious', volume, position)
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
        leshySound('frustrated', volume, position)

    if not skippable:
        waitUntil("leshyTalking",["^J","z"," "], triangle=True)
        SetEyes("Open")
        clearLine(-27)
        sleep(0.5)
    else:
        @threaded
        def endingEyesNonSkip(OldSpeech):
            waitTimerSecs(3)
            if speech == OldSpeech:
                clearLine(-27)
                SetEyes("Open")
        endingEyesNonSkip(speech)