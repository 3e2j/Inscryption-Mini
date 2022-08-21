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


# open our wave file
soundfile = oalOpen(f'{working_directory}/sounds/mono/scale/scale_tick.ogg')
Source.set_gain(soundfile, 1)
Source.set_position(soundfile, (-0.2, 0, 2))

# and start playback
soundfile.play()

# check if the file is still playing
while soundfile.get_state() == AL_PLAYING:
	# wait until the file is done playing
	sleep(1) # lag reducer

# release resources (don't forget this)
oalQuit()