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
			if LoopValue:
				# pyoggSetStreamBufferSize(4096 * 4)
				# oalSetStreamBufferCount(12)
				soundfile = preInitLongSounds[sound_path]  # Path grab
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
					soundfile.play()
					# release resources
				soundfile.stop()
				StopSoundList.remove(LoopValue) #
			else: #Same as loop code but without LoopSound check
				while soundfile.get_state() == AL_PLAYING:
					sleep(1)
				soundfile.destroy()

			if Developer_Mode:
				unicurses.mvaddstr(10, 0, f'Sound Ended: {sound_path}.ogg		') # {working_directory}/sounds/stereo/leshy/
	except:
		pass

#Long Sounds

cabin_ambience = oalOpen(f'{working_directory}/sounds/stereo/cabin/cabin_ambience.ogg')
gametable_ambience = oalOpen(f'{working_directory}/sounds/stereo/cabin/gametable_ambience.ogg')
gametable_ambience2 = oalOpen(f'{working_directory}/sounds/stereo/cabin/gametable_ambience2.ogg')

preInitLongSounds = { #Any Sounds with Looping
	"stereo/cabin/cabin_ambience":cabin_ambience,
	"stereo/cabin/gametable_ambience":gametable_ambience,
	"stereo/cabin/gametable_ambience2":gametable_ambience2
}

#Preloads all of leshy's sounds to stop buffer issues
voice_calm1 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#1.ogg')
voice_calm2 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#2.ogg')
voice_calm3 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#3.ogg')
voice_calm4 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#4.ogg')
voice_calm5 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#5.ogg')
voice_calm6 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#6.ogg')
voice_calm7 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#7.ogg')
voice_calm8 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#8.ogg')
voice_calm9 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#9.ogg')
voice_calm10 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#10.ogg')
voice_calm11 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#11.ogg')
voice_calm12 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_calm#12.ogg')

voice_curious1 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#1.ogg')
voice_curious2 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#2.ogg')
voice_curious3 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#3.ogg')
voice_curious4 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#4.ogg')
voice_curious5 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#5.ogg')
voice_curious6 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#6.ogg')
voice_curious7 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#7.ogg')
voice_curious8 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#8.ogg')
voice_curious9 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#9.ogg')
voice_curious10 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#10.ogg')
voice_curious11 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_curious#11.ogg')

voice_frustrated1 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#1.ogg')
voice_frustrated2 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#2.ogg')
voice_frustrated3 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#3.ogg')
voice_frustrated4 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#4.ogg')
voice_frustrated5 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#5.ogg')
voice_frustrated6 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#6.ogg')
voice_frustrated7 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#7.ogg')
voice_frustrated8 = oalOpen(f'{working_directory}/sounds/stereo/leshy/voice_frustrated#8.ogg')

choicesCalm = [
		voice_calm1,
		voice_calm2,
		voice_calm3,
		voice_calm4,
		voice_calm5,
		voice_calm6,
		voice_calm7,
		voice_calm8,
		voice_calm9,
		voice_calm10,
		voice_calm11,
		voice_calm12
	]

choicesCurious = [
		voice_curious1,
		voice_curious2,
		voice_curious3,
		voice_curious4,
		voice_curious5,
		voice_curious6,
		voice_curious7,
		voice_curious8,
		voice_curious9,
		voice_curious10,
		voice_curious11
	]
choicesFrustrated = [
		voice_frustrated1,
		voice_frustrated2,
		voice_frustrated3,
		voice_frustrated4,
		voice_frustrated5,
		voice_frustrated6,
		voice_frustrated7,
		voice_frustrated8
	]
import random
@threaded
def leshySound(tone, volume=0.4, position=(0,0,0)):
	try:
		if tone == 'calm':
			soundfileLeshy = random.choice(choicesCalm)
		if tone == 'curious':
			soundfileLeshy = random.choice(choicesCurious)
		if tone == 'frustrated':
			soundfileLeshy = random.choice(choicesFrustrated)
		Source.set_gain(soundfileLeshy, volume)
		Source.set_pitch(soundfileLeshy, round(random.uniform(0.95,1.05),2)) # adds dynamic
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