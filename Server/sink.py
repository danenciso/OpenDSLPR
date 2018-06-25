import sys, threading, library, numpy, cv2, time, socket, datetime, thread, os, signal
from PIL import Image
from recognition import Recognize
import server_push

class Structure():
	socket = library.Transmission(int(sys.argv[1]), int(sys.argv[2]))
	ring_buffer = library.Ring_Buffer(int(sys.argv[3]))
	clients_sockets_array = [0]*socket.no_of_conn
	open_alpr = Recognize(int(sys.argv[4]), "ca", os.getcwd())
	complete = False
	frame_rate = library.CalculateRate(1000)  #initial wait time is 1 sec


class Connection(Structure):
	def _connect(self):
		Structure.socket.plug.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		Structure.socket.plug.bind(('', Structure.socket.port))		 							
		Structure.socket.plug.listen(Structure.socket.no_of_conn)
		print("Server {} is ready to receive...".format(Structure.socket.host_ip))
		Structure.clients_sockets_array[0], client_address = Structure.socket.plug.accept()
		print("Connected to {}".format(client_address[0]))
		time.sleep(2)

	def _disconnect(self):
		while 1:
			if Structure.complete:
				Structure.socket.plug.shutdown(1)
				Structure.socket.plug.close()
				sys.exit()

class ReceiveFrames(Structure):
	def __init__(self):	
		self.number_of_frames = 0
	
	def _get_stream(self):
		print("Receiving stream....")
		next_frame_string, current_frame_string = b'', b''
		while not Structure.complete:
			self.number_of_frames += 1
			current_frame_string, next_frame_string = self.__utility(current_frame_string, Structure.clients_sockets_array[0], True)
			np_array = numpy.fromstring(current_frame_string, numpy.uint8)
			current_frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
			
			if type(current_frame) is not type(None): 
				self.__insert_in_ring_buffer(current_frame)

			current_frame_string = next_frame_string
		print("\nNo of frames {}".format(self.number_of_frames))
		print("-----------------------------------------------------------------------All frames received-----------------------------------------------------")

	def __utility(self, data, client, run):
		next_frame_string = b''
		while run:
			try: 
				string = client.recv(9999)   						
				if len(string) == 0:
					print("Length of frame is zero")
					break
					
				index = string.find('STOP!')
				if index != -1:
					data += string[:index]
					run = False
					Structure.complete = True
					
				index = string.find('END!')
				if index != -1:
					data += string[:index]
					next_frame_string = string[index + 4:]
					break					
					
				data += string
			except:
				print("Exception: cature failed")
				continue
		return data, next_frame_string
	
	def __insert_in_ring_buffer(self, frame):            
		Structure.ring_buffer.lock1.acquire()
		fwd = Structure.ring_buffer.head + 1
		if fwd == Structure.ring_buffer.length: fwd = 0
		while fwd == Structure.ring_buffer.tail:
			Structure.ring_buffer.lock1.wait()
		Structure.ring_buffer.push(Structure.ring_buffer.head, frame)
		Structure.ring_buffer.head = fwd
		Structure.ring_buffer.lock1.notify()
		Structure.ring_buffer.lock1.release()           

class AlprProcessing(Structure):
	def __init__(self):
		self.interval = int(sys.argv[6]) #averge of 10 frames

	def _put_alpr(self):
		self.__remove_from_ring_buffer()
		print("--------------------------------------------------------------------End of Alpr processing-------------------------------------------------------")

	def __remove_from_ring_buffer(self):
		current_time_sum = 0
		frame_counter = 0
		array = [0]*self.interval
		while 1:
			Structure.ring_buffer.lock1.acquire()
			if Structure.ring_buffer.tail == Structure.ring_buffer.head and Structure.complete:
				Structure.ring_buffer.lock1.release()
				break
			while Structure.ring_buffer.tail == Structure.ring_buffer.head:
				Structure.ring_buffer.lock1.wait()
			fwd = Structure.ring_buffer.tail + 1
			if fwd == Structure.ring_buffer.length: fwd = 0
			frame = Structure.ring_buffer.pull(Structure.ring_buffer.tail)
			Structure.ring_buffer.tail = fwd
			Structure.ring_buffer.lock1.notify()
			Structure.ring_buffer.lock1.release() 

			start = time.time()                   
			Structure.open_alpr.put(frame)
			end = time.time()

			if frame_counter == self.interval:
				Structure.frame_rate.lock2.acquire()
				Structure.frame_rate._update(current_time_sum / self.interval)
				Structure.frame_rate.lock2.release()
				current_time_sum = 0
				frame_counter = 0
				print(array)
				array = [0]*self.interval
			else:
				current_time_sum += (end - start)
				frame_counter += 1
			array[frame_counter-1] = int((end - start)*10)

class FrameRateUpdateService(Structure):
	def __init__(self):
		self.socket_frame_rate_service = server_push.PushFrameRate(int(sys.argv[5]))

	def _send_update(self):
		while 1:
			client_socket = self.socket_frame_rate_service._return_client_socket()
			data = client_socket.recv(42)
			data = data[:data.find('#')]
			print("Connected to camera node {} for update of frame rate".format(int(data)))
			Structure.frame_rate.lock2.acquire()
			wait_time = Structure.frame_rate._read()
			Structure.frame_rate.lock2.release()
			client_socket.send('{:0<4}'.format(wait_time) + '#')    #miliseconds and adding delimiter
			print("New frame rate is sent to camera node {}".format(int(data)))




