import winsound
from __main__ import working_directory


winsound.PlaySound(f"{working_directory}/sounds/cabin/cabin_ambience.wav", winsound.SND_ASYNC)
a = input("")
if a:
    winsound.PlaySound(None, winsound.SND_PURGE) # Kills all sound