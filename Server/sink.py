import settings, threading, numpy, cv2, time, datetime, thread, signal, sys, os, zmq
from recognition import Recognize
from utils import RingBuffer
from PIL import Image	

class Config():
	def __init__(self):
		self.host_ip = sys.argv[1]
		self.control_ip = settings.server['controller_ip']

		#sets a limit on number of clients that can connect to a server
		self.no_of_conn = int(settings.server['no_of_conn'])

		#a structure consisting of identities of clients
		self.client_list = []

		#servID must be updated after JOIN request to controller
		self.servID = "0" 

		#client specific - may need to be pushed to another client specific class
		self.ring_buffer = RingBuffer(int(settings.server['buffer_size']))
		self.open_alpr = Recognize(int(settings.server['predictions']), "ca", os.getcwd())
		self.complete = False   #may need revision
		self.msg_count=0 		#only for debug purposes
		
		#Bind server to ports
		context = zmq.Context()
		#To send requests to controller
		self.control_port = settings.server['control_port']
		self.control = context.socket(zmq.REQ)
		self.control.connect("tcp://"+self.control_ip+":"+self.control_port)

		#To respond to requests of client(s)
		self.command_port = settings.server['command_port']
		self.command = context.socket(zmq.REP)
		self.command.bind("tcp://"+self.host_ip+":"+self.command_port)

		#To pull frames from client(s)
		self.data_port = settings.server['data_port']
		self.receiver = context.socket(zmq.PULL)
		self.receiver.bind("tcp://"+self.host_ip+":"+self.data_port)

class ReceiveFrames():
	def _get_stream(self,config):
		print("Ready to receive stream....")
		while not config.complete:
			self.current_frame_string = self.__utility(config, True)
			self.np_array = numpy.fromstring(self.current_frame_string, numpy.uint8)
			self.current_frame = cv2.imdecode(self.np_array, cv2.IMREAD_COLOR)
			
			if type(self.current_frame) is not type(None): 
				self.__insert_in_ring_buffer(config, self.current_frame)

		print("frames received = "+str(config.msg_count))
		print("--------------------All frames received----------------------")

	def __utility(self, config, run):
		data = b''
		while run:
			try: 
				string = config.receiver.recv()   						
				if len(string) == 0:
					print("Length of frame is zero")
					break
				
				index = string.find('END!')
				if index != -1:
					data += string[:index]
					config.msg_count = config.msg_count+1
					#print(".") #just to see the progress
					#print("END of frame received")
					break	

				index = string.find('STOP!')
				if index != -1:
					data += string[:index]
					run = False
					config.complete = True
					print("STOP received")				
				
				data += string
			except:
				print("Exception: capture failed")
				continue
		return data
	
	def __insert_in_ring_buffer(self, config, frame):            
		config.ring_buffer.lock.acquire()
		fwd = config.ring_buffer.head + 1
		if fwd == config.ring_buffer.length: fwd = 0
		while fwd == config.ring_buffer.tail:
			config.ring_buffer.lock.wait()
			#print("I am full")

		config.ring_buffer.push(config.ring_buffer.head, frame)
		config.ring_buffer.head = fwd
		#print("pushed to ring_buffer")
		config.ring_buffer.lock.notify()
		config.ring_buffer.lock.release()           

class AlprProcessing():
	def _put_alpr(self, config):
		self.__remove_from_ring_buffer(config)
		#print("in put_alpr")
		print("-------------------End of Alpr processing------------------")

	def __preprocess(self, frame): 
		return frame

	def __remove_from_ring_buffer(self, config):
		while 1:
			#print("Inside remove block")
			config.ring_buffer.lock.acquire()
			if config.ring_buffer.tail == config.ring_buffer.head and config.complete:
				config.ring_buffer.lock.release()
				break
			while config.ring_buffer.tail == config.ring_buffer.head:
				config.ring_buffer.lock.wait()

			fwd = config.ring_buffer.tail + 1
			if fwd == config.ring_buffer.length: fwd = 0
			frame = config.ring_buffer.pull(config.ring_buffer.tail)
			config.ring_buffer.tail = fwd
			config.ring_buffer.lock.notify()
			config.ring_buffer.lock.release()                    
			config.open_alpr.put(self.__preprocess(frame))
