import threading
from threading import Thread

from __main__ import Developer_Mode

'''
This threading engine was built up to run the code IN ITS ORIGINAL SCRIPT.
It doesn't run the code in here. This is simply used as a threading
relocater so the code doesn't have to be remade in every single script.
'''

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        # Removed old loop code: better to control from inside the func itself instead of threading func
        thread.start()
    return wrapper
