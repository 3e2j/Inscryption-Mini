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
Recommended just to use Audacity and multiple-export files after conversion
'''


from engine.threadingEngine import threaded

GlobalCheckList = []

@threaded
def StopLoopingSound(LoopValue):
	global GlobalCheckList
	GlobalCheckList.append(LoopValue)

@threaded
def PlaySound(sound_path, volume, position, LoopValue):
	from __main__ import Developer_Mode
	if Developer_Mode:
		import unicurses
		unicurses.mvaddstr(9, 0, f'Last played: {sound_path}.ogg') # {working_directory}/sounds/

	soundfile = oalOpen(f'{working_directory}/sounds/{sound_path}.ogg')
	Source.set_gain(soundfile, volume)
	if position:
		Source.set_position(soundfile, position)
	soundfile.play()

	if LoopValue:
		while LoopValue not in GlobalCheckList:

				# check if the file is still playing
			while soundfile.get_state() == AL_PLAYING and LoopValue not in GlobalCheckList:
				# wait until the file is done playing
				sleep(1) # lag reducer
			# release resources
			oalQuit()
		GlobalCheckList.remove(LoopValue)
	else:
		while soundfile.get_state() == AL_PLAYING:
			sleep(1)
		oalQuit()