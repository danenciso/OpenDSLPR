#!/usr/bin/env python
import settings, sys, os, zmq, time, threading, thread	
from serv_manage import ManageServers
from client_manage import ManageClients

class Config():
	def __init__(self):
		self.host_ip = settings.controller['ip_add']
		# {servID: no_of_clients, servID:2}
		self.serv_load = dict()

		# {servID:[IP_address, port, clientID, clientID,...], servID:[...]}
		self.serv_meta = dict()
		
		# [clientID, clientID,...]
		self.client_list = []

		self.context = zmq.Context()
		'''
		- To communicate with server(s) by sending OUT requests
		- This socket sends commands to server(s)
		- IP address and port will be provided by other internal methods
		- To have reliable working of the REQ-REP pattern, in ZMQ terminology, this socket must
		  zmq.connect() and then zmq.disconnect() to/from the server IP address  
		'''
		self.command = self.context.socket(zmq.REQ)

		'''
		- To communicate with server(s) by sending OUT replies
		- This socket LISTENS for requests from servers and replies accordingly
		'''
		self.serv_reply_port = settings.controller['serv_control_port']
		self.serv_control = self.context.socket(zmq.ROUTER)
		self.serv_control.bind("tcp://"+self.host_ip+":"+self.serv_reply_port)

		'''
		- To communicate with client(s) by sending OUT replies
		- This socket LISTENS for requests from clients and replies accordingly
		'''
		self.client_reply_port = settings.controller['client_control_port']
		self.client_control = self.context.socket(zmq.ROUTER)
		self.client_control.bind("tcp://"+self.host_ip+":"+self.client_reply_port)

if __name__ == '__main__':
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