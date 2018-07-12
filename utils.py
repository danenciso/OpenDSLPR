import threading, thread

class Control():
	@staticmethod
	def _join(config):
		config.control.send("JOIN!"+config.servID+config.host_ip+":"+config.command_port)
		receive = config.control.recv()
		print("in response to join received "+receive)
		if receive[:4]=="200!":
			print(receive)
			config.servID = receive[4:]
		else:
			print("ERROR")

	@staticmethod
	def _scan(config):
		receive = config.command.recv()
		#print(receive)
		if receive=="CHECK!":
			print("Controller nudged me with CHECK!")
			config.command.send("200!")
		else:
			config.command.send("400!")

class ManageClients():
	def _scan(self, config):
		self.request = config.command.recv()
		if self.request[:8] == "CONNECT!":
			if len(config.client_list)<config.no_of_conn:
				config.client_list.append(self.request[8:])
				self.reply = "200!"+config.data_port							#200 - SUCCESS
				#print("Sending reply as "+self.reply)
				config.command.send(self.reply)
			else:
				config.command.send("503!")										#503 - Service Unavailable, connection limit reached 
		else:
			config.command.send("400!")											#400 - Bad request

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