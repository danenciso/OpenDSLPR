import os, sys, zmq, numpy, cv2, time
from PIL import Image

class Transmit():
	def __init__(self, server_ip, port):  #socket initialization
		self.sender = context.socket(zmq.PUSH)
		self.host_ip = "tcp://" + server_ip
		self.port = port
		
	def connection(self):    #making connection
		self.sender.connect(self.host_ip+":"+str(self.port))
		print("Connected to "+self.host_ip[6:]+":"+str(self.port))

	def send(self, video_file):  #sending frames 
		capture = cv2.VideoCapture(os.getcwd() + "/" + video_file)            #capturing the video
		count=0
		while 1:
			return_val, frame = capture.read()   #breaking into frames
			if return_val:
				data = cv2.imencode('.jpg', frame)[1].tostring()   #numpy func converting into bytes(not string)(name tostring is misleading)
				self.sender.send(data + 'END!')
				count=count+1
				time.sleep(0.01)
			else:
				self.sender.send('STOP!')
				print("Number of frames sent = "+str(count))
				break
		time.sleep(1)
		capture.release()
		print("--------------End of frame parsing--------------")

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python <script_name> <server_address> <port> <name_of_video_file>")
		sys.exit()

	context = zmq.Context()
	node = Transmit(sys.argv[1], int(sys.argv[2]))
	node.connection()
	node.send(sys.argv[3])