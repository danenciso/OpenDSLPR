#!/usr/bin/env python
import sys, os, zmq, time, threading, thread	
from serv_manage import ManageServers
from client_manage import ManageClients

class Config():
	def __init__(self):
		self.host_ip = sys.argv[1]
		# {servID: no_of_clients, servID:2}
		self.serv_load = dict()
		# {servID:[IP_address, port, clientID, clientID,...], servID:[...]}
		self.serv_meta = dict()
		# [clientID, clientID,...]
		self.client_list = []

		self.context = zmq.Context()
		#To communicate with server(s) by sending OUT requests
		#This socket sends commands to server(s)
		#IP address and port will be provided by server in its JOIN request
		self.command = self.context.socket(zmq.REQ)
		

		#To communicate with server(s) by sending OUT replies
		#This socket LISTENS for requests from servers and replies accordingly
		self.serv_reply_port = sys.argv[2]
		self.serv_control = self.context.socket(zmq.ROUTER)
		self.serv_control.bind("tcp://"+self.host_ip+":"+self.serv_reply_port)

		#To communicate with client(s) by sending OUT replies
		#This socket LISTENS for requests from clients and replies accordingly
		self.client_reply_port = sys.argv[3]
		self.client_control = self.context.socket(zmq.ROUTER)
		self.client_control.bind("tcp://"+self.host_ip+":"+self.client_reply_port)

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage : python <script_name> <IP_address> <Server-Reply-Port> <Client-Reply-Port>")
		sys.exit()

	do_exit = False
	ctrl_config = Config()
	print("Controller is listening for requests ...")

	#create objects for both classes
	#The object instatiation spawns a thread in the constructor for that object 
	ManageServer = ManageServers(ctrl_config)
	ManageClient = ManageClients(ctrl_config)

	while do_exit==False:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			do_exit = True

	#the stop method of these objects internally stops the thread and waits until the thread joins
	ManageClient.stop()
	ManageServer.stop()
	ctrl_config.serv_control.close()
	ctrl_config.client_control.close()