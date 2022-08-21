from __main__ import working_directory
# import PyOpenAL (will require an OpenAL shared library)
from openal import *
from openal import Source#Just makes my life easier

# import the time module, for sleeping during playback
from time import sleep

'''
Quick note:
Any directional based sound must have the soundfile as mono, not stereo.
No, there is no quick way to convert these in this soundEngine.
Recommended just to use Audacity and multiple-export files after conversion.

OpenAL doesn't support mp3, originally used wav files but converted to ogg to compress files
and bypass git-hub's upload limit per file (100MB)
Due to ogg being 'partially' unsuppoted by OpenAL, it requires pyogg to be installed. (see initboot.bat)
'''


from engine.threadingEngine import threaded

StopSoundList = [] #Threaded sounds store their values in this list when being stopped

@threaded
def StopLoopingSound(LoopValue): #Store value in StopSoundList
	global StopSoundList
	StopSoundList.append(LoopValue)

@threaded
def PlaySound(sound_path, volume, position, LoopValue=False):
	from __main__ import Developer_Mode
	if Developer_Mode:
		import unicurses
		unicurses.mvaddstr(9, 0, f'Last played: {sound_path}.ogg') # {working_directory}/sounds/

	soundfile = oalOpen(f'{working_directory}/sounds/{sound_path}.ogg') #Path grab
	Source.set_gain(soundfile, volume) #Volume
	if position:
		Source.set_position(soundfile, position) #3D audio, if pos is False, will play normal (0,0,0)

	soundfile.play()

	if LoopValue: #Looping sounds (IE: Music)
		while LoopValue not in StopSoundList: #Loop until trigger
			while soundfile.get_state() == AL_PLAYING and LoopValue not in StopSoundList: # check if the file is still playing
				# wait until the file is done playing
				sleep(1) # lag reducer
			# release resources
			oalQuit()
		StopSoundList.remove(LoopValue) #
	else: #Same as loop code but without StopLoopingSound check
		while soundfile.get_state() == AL_PLAYING:
			sleep(1)
		oalQuit()

	if Developer_Mode:
		import unicurses
		unicurses.mvaddstr(10, 0, f'Sound Ended: {sound_path}.ogg') # {working_directory}/sounds/
