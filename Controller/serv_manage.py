#!/usr/bin/env python
import zmq, threading, thread, time
from controller_utils import StoppableThread

class ManageServers(StoppableThread):
	def __init__(self, config):
		StoppableThread.__init__(self)
		self.thread = threading.Thread(name="Listen_server_requests", target=self.run, args=(config,))
		self.thread.start()

	def run(self, config):
		while self.stop_event.is_set()==False:
			self._join(config)

	def _join(self, config):
		server, empty, receive = config.serv_control.recv_multipart()
		print("Received "+receive)
		if receive[:5] == "JOIN!" and receive[5]=="0":
			try:
				config.command.connect("tcp://"+receive[6:])
				req = "CHECK!"+receive[6:]
				config.command.send(req)
				#print("Sent CHECK! to server on tcp://"+receive[6:])
				reply = config.command.recv()
				print("in response to nudge, received from server "+reply)

				while reply == "400!":
					#retry nudging the server
					config.command.connect("tcp://"+receive[6:])
					req = "CHECK!"+receive[6:]
					config.command.send(req)
					print("Resent CHECK! to server on tcp://"+receive[6:])
					reply = config.command.recv()
					print("in response to nudge, received from server "+reply)

				
				if reply == "200!":
					if not config.serv_meta:
						#serv_meta empty
						servID = "s100"
					else:
						serv_list = sorted(config.serv_meta)
						servID = "s"+str(int(serv_list[-1][1:])+1)

					config.serv_meta[servID] = receive[6:].split(":")
					print(config.serv_meta)
					config.serv_load[servID] = 0
					print(config.serv_load)
					msg = "200!"+servID
					print(msg)
					config.serv_control.send_multipart([server, "", msg])

			except:
				#400 - Bad request
				config.serv_control.send_multipart([server, "", "400!"])

			#for reliable working of REQ-REP
			config.command.disconnect("tcp://"+receive[6:])
			

		elif receive[:-1] == "DISJOIN!" and receive[-1]!="0":
			print("feature coming soon")