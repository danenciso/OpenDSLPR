import threading, thread

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()        

    def stop(self):
    	print("Stop thread called")
        if self.mythread.is_alive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            print("Server: Preparing to stop a thread, waiting on join")
            # block calling thread until thread really has terminated
            self.mythread.join()
        else:
        	print("Server: ERROR")

#Spawns thread for scanning requests/commands from controller and responds to those
class Scan(StoppableThread):
	def __init__(self, config):
		StoppableThread.__init__(self)
		self.mythread = threading.Thread(name="Listen_controller_commands", target=self.run, args=(config,))
		self.mythread.start()

	def run(self, config):
		#stop_event inherited from StoppableThread class
		while self.stop_event.is_set()==False:
			self._scan(config)

	def _scan(self, config):
		receive = config.command.recv()
		print(receive)
		#print("checking for "+"CHECK!"+config.host_ip+config.command_port)
		if receive=="CHECK!"+config.host_ip+":"+config.command_port:
			print("Controller: CHECK!")
			config.command.send("200!")
			print("Server: 200!")

		#Connect clients to server
		elif receive[:8] == "CONNECT!":
			if len(config.client_list)<config.no_of_conn:
				config.client_list.append(receive[8:])
				reply = "200!"+config.data_port
				#print("Sending reply as "+self.reply)
				#200 - SUCCESS
				config.command.send(reply)
			else:
				#503 - Service Unavailable, connection limit reached
				config.command.send("503!") 

		elif receive[:11] == "DISCONNECT!":
			if receive[11:] in config.client_list:
				config.client_list.remove(receive[11:])
				print("Server: client "+receive[11:]+" disconnected")
				config.command.send("200!")
			else:
				config.command.send("400!")
		else:
			#400 - Bad request
			config.command.send("400!")
			print("Server: 400!")

class Control():
	@staticmethod
	def _join(config):
		config.control.send("JOIN!"+config.servID+config.host_ip+":"+config.command_port)
		receive = config.control.recv()
		print("Controller: "+receive)
		if receive[:4]=="200!":
			#print(receive)
			config.servID = receive[4:]
		else:
			print("Server: ERROR")

class RingBuffer():
	def __init__(self, size):
		self.buffer = [None]*size
		self.lock = threading.Condition(threading.Lock())
		self.head = 0
		self.tail = 0
		self.length = size

	def push(self, index, frame):
		self.buffer[index] = frame
 
	def pull(self, index):
		 return self.buffer[index]