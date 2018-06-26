import threading, utils, numpy, cv2, time, datetime, thread, signal
from PIL import Image	

class ReceiveFrames():
	def _get_stream(self,config):
		print("Receiving stream....")
		
		while not config.complete:
			self.current_frame_string = self.__utility(config, True)
			self.np_array = numpy.fromstring(self.current_frame_string, numpy.uint8)
			self.current_frame = cv2.imdecode(self.np_array, cv2.IMREAD_COLOR)
			
			if type(self.current_frame) is not type(None): 
				self.__insert_in_ring_buffer(config, self.current_frame)

		print("Frames received = "+str(config.msg_count))
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
					break	

				index = string.find('STOP!')
				if index != -1:
					data += string[:index]
					run = False
					config.complete = True			
				
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
