from __main__ import TurnOffSoundForLinux
# import PyOpenAL (will require an OpenAL shared library)
if not TurnOffSoundForLinux:
	from openal import *
	from openal import Source#Just makes my life easier

# import the time module, for sleeping during playback
from time import sleep
import unicurses

from random import choice


'''
Quick note:
Any directional based sound must have the soundfile as mono, not stereo.
No, there is no quick way to convert these in this soundEngine.
Recommended just to use Audacity and multiple-export files after conversion.

OpenAL doesn't support mp3, originally used wav files but converted to ogg to compress files
and bypass git-hub's upload limit per file (100MB)
Due to ogg being 'partially' unsuppoted by OpenAL, it requires pyogg to be installed. (see __main__)
'''


from engine.threadingEngine import threaded

StopSoundList = [] #Threaded sounds store their values in this list when being stopped

def KillAllSounds():
	if not TurnOffSoundForLinux:
		oalQuit()

def StopLoopingSound(LoopValue): #Store value in StopSoundList
	global StopSoundList
	StopSoundList.append(LoopValue)

from __main__ import Developer_Mode, working_directory
from unicurses import mvaddstr


@threaded
def PlaySound(sound_path, volume=1, position=(0,0,0), LoopValue=False, pitch = 1): #*args
	global StopSoundList
	try:
		if not TurnOffSoundForLinux:
			DestroySoundSource = True
			if LoopValue:
				soundfile = preInitLongSounds[sound_path]  # Path grab
			else:
				if sound_path in preInitSounds.keys():
					DestroySoundSource = False
					soundfile = preInitSounds[sound_path]  # Path grab
				else:
					soundfile = oalOpen(f'{working_directory}/sounds/{sound_path}.ogg')  # Path grab

			Source.set_gain(soundfile, volume) #Volume
			Source.set_position(soundfile, position) #3D audio, if pos is False, will play normal (0,0,0)
			Source.set_pitch(soundfile, pitch)
			soundfile.play()
			if Developer_Mode:
				unicurses.mvaddstr(9, 0, f'Last played: {sound_path}.ogg {LoopValue}		') # {working_directory}/sounds/stereo/leshy/

			if LoopValue: #Looping sounds (IE: Music)
				while LoopValue not in StopSoundList: #Loop until trigger
					while soundfile.get_state() == AL_PLAYING and LoopValue not in StopSoundList: # check if the file is still playing
						# wait until the file is done playing
						sleep(1)
					if LoopValue not in StopSoundList:
						soundfile.play()
				soundfile.stop()
				StopSoundList.remove(LoopValue)
			else: #Same as loop code but without LoopSound check
				while soundfile.get_state() == AL_PLAYING:
					sleep(1)
				if DestroySoundSource:
					soundfile.destroy()

			if Developer_Mode:
				unicurses.mvaddstr(10, 0, f'Sound Ended: {sound_path}.ogg		') # {working_directory}/sounds/stereo/leshy/
	except:
		pass
'''
Pre-loaded Sounds.
Caches soundfiles into memory to stop noticable buffer-times for long sounds.

oalOpen only loads the sound as one ID into memory slot.
If sound is triggered again, will cancel old sound and play from start.
Should not be used if overlapping sounds is required. (Refer to sacrifice_defaultPRELOADED)
'''
#Long Sounds
preInitLongSounds = { #Any Sounds with Looping
	"stereo/cabin/cabin_ambience":oalOpen(f'{working_directory}/sounds/stereo/cabin/cabin_ambience.ogg'),
	"stereo/cabin/gametable_ambience":oalOpen(f'{working_directory}/sounds/stereo/cabin/gametable_ambience.ogg'),
	"stereo/cabin/gametable_ambience2":oalOpen(f'{working_directory}/sounds/stereo/cabin/gametable_ambience2.ogg')
}
#Short Sounds
preInitSounds = {
	#Preloaded Sacrifice Sound
	"mono/card/sacrifice_defaultPRELOADED":oalOpen(f'{working_directory}/sounds/mono/card/sacrifice_default.ogg'),
	#Cards
	"mono/card/card#1":oalOpen(f'{working_directory}/sounds/mono/card/card#1.ogg'),
	"mono/card/card#2":oalOpen(f'{working_directory}/sounds/mono/card/card#2.ogg'),
	"mono/card/card#3":oalOpen(f'{working_directory}/sounds/mono/card/card#3.ogg'),
	"mono/card/card#4":oalOpen(f'{working_directory}/sounds/mono/card/card#4.ogg'),
	"mono/card/card#5":oalOpen(f'{working_directory}/sounds/mono/card/card#5.ogg'),
	"mono/card/card#6":oalOpen(f'{working_directory}/sounds/mono/card/card#6.ogg'),
	"mono/card/card#7":oalOpen(f'{working_directory}/sounds/mono/card/card#7.ogg'),
	"mono/card/card#8":oalOpen(f'{working_directory}/sounds/mono/card/card#8.ogg'),
	"mono/card/card#9":oalOpen(f'{working_directory}/sounds/mono/card/card#9.ogg'),
	"mono/card/card#10":oalOpen(f'{working_directory}/sounds/mono/card/card#10.ogg'),
	"mono/card/cardquick#1":oalOpen(f'{working_directory}/sounds/mono/card/cardquick#1.ogg'),
	"mono/card/cardquick#2":oalOpen(f'{working_directory}/sounds/mono/card/cardquick#2.ogg'),
	"mono/card/cardquick#3":oalOpen(f'{working_directory}/sounds/mono/card/cardquick#3.ogg'),
	"mono/card/cardquick#4":oalOpen(f'{working_directory}/sounds/mono/card/cardquick#4.ogg'),
	#Candle
	"mono/candle/candle_gainLife":oalOpen(f'{working_directory}/sounds/mono/candle/candle_gainLife.ogg'),
	"mono/candle/candle_loseLife":oalOpen(f'{working_directory}/sounds/mono/candle/candle_loseLife.ogg')
}


#Preloads all of leshy's sounds to stop buffer issues

choicesCalm = [
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#1.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#2.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#3.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#4.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#5.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#6.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#7.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#8.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#9.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#10.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#11.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#12.ogg')
	]

choicesCurious = [
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#1.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#2.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#3.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#4.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#5.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#6.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#7.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#8.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#9.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#10.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#11.ogg')
	]
choicesFrustrated = [
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#1.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#2.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#3.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#4.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#5.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#6.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#7.ogg'),
	oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#8.ogg')
	]

from random import choice, uniform
@threaded
def leshySound(tone, volume=0.4, position=(0,0,0)):
	try:
		if tone == 'calm':
			soundfileLeshy = choice(choicesCalm)
		if tone == 'curious':
			soundfileLeshy = choice(choicesCurious)
		if tone == 'frustrated':
			soundfileLeshy = choice(choicesFrustrated)
		Source.set_gain(soundfileLeshy, volume)
		Source.set_pitch(soundfileLeshy, round(uniform(0.95,1.05),2)) # adds dynamic
		Source.set_position(soundfileLeshy, position)
		if Developer_Mode:
			unicurses.mvaddstr(9, 0, f'Last played: leshy {tone}		')
		soundfileLeshy.play()
		while soundfileLeshy.get_state() == AL_PLAYING:
			sleep(1)
		if Developer_Mode:
			unicurses.mvaddstr(10, 0, f'Sound Ended: leshy {tone}		')
	except Exception:
		print(Exception)

def CardPlaySound(tone="normal", position=(0,0,0), volume=0.7):
    if tone == "normal":
        normal = [
            "card#1",
            "card#2",
            "card#3",
            "card#4",
            "card#5",
            "card#6",
            "card#7",
            "card#8",
            "card#9",
            "card#10"
        ]
        PlaySound(f"mono/card/{choice(normal)}", volume, position)
    if tone == "quick":
        quick = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{choice(quick)}", volume, position)
    if tone == "glow":
        glow = [
            "cardslot_glow#1",
            "cardslot_glow#2",
            "cardslot_glow#3",
            "cardslot_glow#4"
        ]
        PlaySound(f"mono/card/{choice(glow)}", volume, position)