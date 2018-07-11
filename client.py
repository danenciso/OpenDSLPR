#Compression
import os
import sys
import zmq
from PIL import Image
import sys, numpy, cv2, time, os

class Transmit():
	def __init__(self, cntrl_address, control_port):
		self.sender = context.socket(zmq.PUSH)
		self.request = context.socket(zmq.REQ)

		self.serv_ip = None									#IP address of server, as received from controller
		self.data_port = None								#Send frames to server
		self.command_port = None							#Send requests to server(if any)
		self.control_port = control_port					#Send control requests to controller
		self.cntrl_ip = cntrl_address
		self.identity = 0
		
	
	#Send requests to controller - Ping the controller
	def ping(self):
		self.request.connect("tcp://"+self.cntrl_ip+":"+str(self.control_port))
		self.request.send("CONNECT!"+str(self.identity))
		print("CONNECT request sent to tcp://"+self.cntrl_ip+":"+str(self.control_port))
		reply = self.request.recv()

		#reply of the form <status><!><6-digit-unique_ID><server_IP:data_port>
		#					200!100000127.0.0.1:5556		(if success)
		#					400!							(if failed)
		if reply[:4]== "200!":
			self.identity = reply[4:10]
			address = reply[10:].split(":")
			self.serv_ip = address[0]
	   		self.data_port = address[1]
	   	 	
	   	 	print("Server accepted the connection")
	   	 	print("I am assigned identity as "+self.identity)
	   	 	return 1
	   	else:
	   		print("ERROR "+reply[:4])
	   		return 0

	def connection(self):
		#self.sender.setsockopt(zmq.SNDHWM, 100)
		self.sender.connect("tcp://"+self.serv_ip+":"+self.data_port)
		print("Connected to tcp://"+self.serv_ip+":"+self.data_port+" for data transfer")

	def send(self, video_file):
		capture = cv2.VideoCapture(os.getcwd() + "/" + video_file)            #capturing the video
		count=0
		while 1:
			return_val, frame = capture.read()   #breaking into frames
			if return_val:
				data = cv2.imencode('.jpg', frame)[1].tostring()   #numpy func converting into bytes(not string)(name tostring is misleading)
				self.sender.send(data+'END!')
				sys.stdout.write(".")
				sys.stdout.flush()
				count=count+1
				time.sleep(0.01)

			else:
				self.sender.send('STOP!')
				print("STOP sent")
				print("number of frames sent = "+str(count))
				break
		
		time.sleep(1)
		capture.release()
		print("--------------End of frame parsing--------------")

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python <script_name> <controller_address> <RRport> <name_of_video_file>")
		sys.exit()

	context = zmq.Context()
	#print("Current libzmq version is %s" % zmq.zmq_version())
	#print("Current  pyzmq version is %s" % zmq.__version__)
	node = Transmit(sys.argv[1], int(sys.argv[2]))
	status = node.ping()
	time.sleep(1)
	if status:
		node.connection()
		node.send(sys.argv[2])
