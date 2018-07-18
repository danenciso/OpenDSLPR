#!/usr/bin/env python
import threading, thread

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()        

    def stop(self):
    	print("Stop thread called")
        if self.thread.is_alive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            print("I have set the stop event")
            # block calling thread until thread really has terminated
            self.thread.join()
        else:
        	print("ERROR")