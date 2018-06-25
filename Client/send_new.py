import sys, threading, thread
from PIL import Image
import socket, sys, numpy, cv2, time, os

class Transmission():
	def __init__(self, data_port, video_file, frame_rate_port):
		try: #Checking connection
			self.plug = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print("Socket creation is failed")
		self.port = data_port
		self.host_ip = "192.168.1.102"
		#self.host_ip = socket.gethostbyname(socket.gethostname()) #gethostname gives string, gethostbyname converts to IPv4
		self.lock = threading.Condition(threading.Lock())
		self.wait_time = 0 #initial 
		self.frame_rate_port = frame_rate_port
		self.run = 1  					#for closing server
		self.filename = video_file
	
	def Connection(self):
		self.plug.connect((self.host_ip, self.port))
		print("Connected to dataserver {}".format(self.host_ip))

	def Send(self):
		capture = cv2.VideoCapture(os.getcwd() + "/" + "v.mp4")            #capturing the video

		while 1:
			return_val, frame = capture.read()   #breaking into frames
			
			self.lock.acquire()
			time.sleep(int(self.wait_time/1000))
			self.lock.release()

			if return_val:
				data = cv2.imencode('.jpg', frame)[1].tostring()   #numpy func converting into bytes(not string)(name tostring is misleading)
				self.plug.send(data + 'END!')
			else:
				self.plug.send("STOP!")
				self.run = 0
				break
		self.plug.shutdown(1)
		self.plug.close()
		capture.release()
		print("-----------------------------------------------------------------End of frame parsing--------------------------------------------------")

	def UpdateFrameRate(self):
		thread_spawn_time = 10  
		while self.run:
			print("\n\nContacting server to get latest frame rate ..."),
			new_connection = send_pull.UpdateWaitingTime(self.frame_rate_port, 0)
			delay = new_connection.get()
			self.lock.acquire()
			self.wait_time = delay
			self.lock.release()
			print("Frame rate updated with wait time {} milisec.".format(delay))
			time.sleep(thread_spawn_time)


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python <script_name> <port> <name_of_video_file> <master_port_for_frame_rate>")
		sys.exit()
	node = Transmission(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
	node.Connection()

	thread0 = threading.Thread(name="Send", target=node.Send)
	thread1 = threading.Thread(name="Update_my_port", target=node.UpdateFrameRate)
	thread0.start()
	thread1.start()
	
