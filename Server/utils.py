import threading, thread, sys, os, zmq
from recognition import Recognize

class Config():
	def __init__(self):
		self.port = int(sys.argv[1])						   				#port to be connected
		self.no_of_conn = int(sys.argv[4])             						#remove if don't want a limit on number of connected clients
		self.clients_sockets_array = [0]*self.no_of_conn 					#a structure consisting of identities of clients
		
		#client specific may need to be pushed to another client specific class
		self.ring_buffer = RingBuffer(int(sys.argv[2]))
		self.open_alpr = Recognize(int(sys.argv[3]), "ca", os.getcwd())
		self.complete = False   											#may need revision
		self.msg_count=0 													#only for debug purposes
		
		# Done with initialization, now bind server to port
		context = zmq.Context()
		self.receiver = context.socket(zmq.PULL)
		self.receiver.bind("tcp://*:"+str(self.port))				#Tcp connection

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





