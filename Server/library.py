import socket, threading, thread

class Transmission():
	def __init__(self, no_of_conn, port):
		self.no_of_conn = no_of_conn               							#no of simultaneous connections by the server
		self.port = port						   							#port to be connected
		self.plug = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  	#Tcp connections
		self.host_ip = socket.gethostbyname(socket.gethostname()) 

class Ring_Buffer():
	def __init__(self, size):
		self.buffer = [None]*size
		self.lock1 = threading.Condition(threading.Lock())
		self.head = 0
		self.tail = 0
		self.length = size

	def push(self, index, frame):
		self.buffer[index] = frame
 
	def pull(self, index):
		 return self.buffer[index]

class CalculateRate():
	def __init__(self, initial_time):
		self.average_time = initial_time
		self.lock2 = threading.Condition(threading.Lock())

	def _update(self, time):
		self.average_time = int(time*1000)  #in miliseconds

	def _read(self):
		return self.average_time


