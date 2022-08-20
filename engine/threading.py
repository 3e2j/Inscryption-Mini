import threading
from threading import Thread
import unicurses
from __main__ import Developer_Mode


# Threaded function snippet
# def threaded(IsLooped):
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)

        # Removed old loop code: better to control from inside the func itself instead of threading func

        try:
            thread.start()
            if Developer_Mode:
                unicurses.mvaddstr(2, 0, f"Successful Threading Setup for {thread}")
            # thread.join()
            # StandardScreen.addstr(20, 0, f"Fully ran through thread")
            # StandardScreen.refresh()
            # time.sleep(50)
            # thread.join() # For calling upon if a thread is completed, just use whatever def is after: refer to game.dialouge.dialouge.startScreen <Dialouge 2>
        except:
            if Developer_Mode:
                unicurses.mvaddstr(2, 0, f"Unsuccesful Threading Setup for {thread}")
        return thread

    return wrapper
    # return threadedInner
