#!/usr/bin/env python
import threading, thread

class ClientConnectRule():
    @staticmethod
    def connect_rule(config, rule):
        #rule = 0 is default rule, which does load balancing
        if rule==0:
            serv_list = sorted(config.serv_load.iteritems(), key=lambda (k,v):(v,k))
            servers = []
            for serv_tuple in serv_list:
                servers.append(serv_tuple[0])
            return servers
        else:
            return []

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()        

    def stop(self):
    	print("Stop thread called")
        if self.thread.is_alive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            print("Controller: Preparing to stop a thread, waiting on join")
            # block calling thread until thread really has terminated
            self.thread.join()
        else:
        	print("ERROR")