#Compression
import os
import sys
from PIL import Image
#Transmission
import socket, sys, numpy, cv2, time, os

class Transmission():
	def __init__(self, port):
		try: #Checking connection
			self.plug = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print("Socket creation is failed")
		self.port = port
		self.host_ip = "10.138.118.12"#socket.gethostbyname(socket.gethostname()) #gethostname gives string, gethostbyname converts to IPv4
		
	def Connection(self):
		print self.host_ip
		print self.port
		self.plug.connect((self.host_ip, self.port))
		print("Connected to {}".format(self.host_ip))

	def Send(self, video_file):
		capture = cv2.VideoCapture(os.getcwd() + "/" + video_file)            #capturing the video
		while 1:
			return_val, frame = capture.read()   #breaking into frames
			if return_val:
				data = cv2.imencode('.jpg', frame)[1].tostring()   #numpy func converting into bytes(not string)(name tostring is misleading)
				self.plug.send(data + 'END!')
			else:
				self.plug.send("STOP!")
				break
		self.plug.shutdown(1)
		self.plug.close()
		capture.release()
		print("-----------------------------------------------------------------End of frame parsing--------------------------------------------------")

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python <script_name> <port> <name_of_video_file>")
		sys.exit()
	node = Transmission(int(sys.argv[1]))
	node.Connection()
	node.Send(sys.argv[2])
