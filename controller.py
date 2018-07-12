import sys, os, zmq, time, threading, thread

class Config():
	def __init__(self):
		self.host_ip = sys.argv[1]
		self.serv_load = dict()											# {servID: no_of_clients, servID:2}
		self.serv_meta = dict()											# {servID:[IP_address, port, clientID, clientID,...], servID:[...]}
		self.client_list = []											# [clientID, clientID,...]

		context = zmq.Context()
		#To communicate with server(s) by sending OUT requests
		#This socket sends commands to server(s)
		#IP address and port will be provided by server in its JOIN request
		self.command = context.socket(zmq.REQ)
		

		#To communicate with server(s) by sending OUT replies
		#This socket LISTENS for requests from servers and replies accordingly
		self.serv_reply_port = sys.argv[2]
		self.serv_control = context.socket(zmq.REP)
		self.serv_control.bind("tcp://"+self.host_ip+":"+self.serv_reply_port)

		#To communicate with client(s) by sending OUT replies
		#This socket LISTENS for requests from clients and replies accordingly
		self.client_reply_port = sys.argv[3]
		self.client_control = context.socket(zmq.REP)
		self.client_control.bind("tcp://"+self.host_ip+":"+self.client_reply_port)

class ManageServers():
	@staticmethod
	def _join(config):
		receive = config.serv_control.recv()
		print("Received "+receive)
		if receive[:5] == "JOIN!" and receive[5]=="0":
			try:
				config.command.connect("tcp://"+receive[6:])
				config.command.send("CHECK!")
				print("Sent CHECK!")
				reply = config.command.recv()
				print(reply)
				if reply == "200!":
					if not config.serv_meta: #empty
						servID = "s100"
					else:
						serv_list = sorted(config.serv_meta)
						servID = "s"+str(int(serv_list[-1][1:])+1)

					config.serv_meta[servID] = receive[6:].split(":")
					#print(config.serv_meta)
					config.serv_load[servID] = 0
					#print(config.serv_load)
					config.serv_control.send("200!"+servID)

			except:
				config.serv_control.send("400!")							#400 - Bad request
			

		elif receive[:-1] == "DISJOIN!" and receive[-1]!="0":
			print("feature coming soon")

class ManageClients():
	@staticmethod
	def _scan(config):
		receive = config.client_control.recv()
		print(receive)
		if receive[:-1] == "CONNECT!" and receive[-1]=="0":				#Ensure the 'connect' request is from a new client
			find_server = sorted(config.serv_load.iteritems(), key=lambda (k,v):(v,k))

			if find_server:
				print("came inside find_server")
				print(find_server)
				if not config.client_list:
					clientID = "100000"
					print("assigned 1st client ID")
				else:
					clientID = config.client_list[-1] + 1

				err_count = 0
				for server,load in find_server:
					print("came inside for loop, connecting to "+config.serv_meta[server][0]+config.serv_meta[server][1])
					config.command.connect("tcp://"+config.serv_meta[server][0]+":"+config.serv_meta[server][1])
					config.command.send("CONNECT!"+clientID)
					reply = config.command.recv()

					#reply consists of server's pull-port
					print("received reply from server "+reply)
					if(reply[:4]=="200!"):
						config.client_list.append(clientID)
						config.serv_meta[server].append(clientID)
						config.serv_load[server] += 1
						data_port = reply[4:8]
						print("Sending reply 200!"+clientID+config.serv_meta[server][0]+":"+data_port)
						config.client_control.send("200!"+clientID+config.serv_meta[server][0]+":"+data_port)		#200 - SUCCESS
						break
					elif reply[:4]=="503!":
						err_count += 1

					elif reply[:4]=="400!":
						config.client_control.send("400!")
				
				if err_count==len(find_server):
					config.client_control.send("503!")							#503 - Service Unavailable, connection limit reached

			else:
				print("No server joined")
				config.client_control.send("503!")

		elif receive[:-1] == "DISCONNECT!" and receive[-1]!="0":		#Ensure the 'disconnect' request is from a valid client
			print("feature coming soon")

		else:
			config.client_control.send("400!")								#400 - Bad request
		

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage : python <script_name> <IP_address> <Server-Reply-Port> <Client-Reply-Port>")
		sys.exit()

	ctrl_config = Config()
	print("Controller is listening for requests ...")

	#while True:
		#ManageServers._join(ctrl_config)
		#ManageClients._scan(ctrl_config)
	thread0 = threading.Thread(name="Listen_server_requests", target=ManageServers._join, args=(ctrl_config,))
	thread1 = threading.Thread(name="Listen_client_requests", target=ManageClients._scan, args=(ctrl_config,))
	thread0.start()
	thread1.start()