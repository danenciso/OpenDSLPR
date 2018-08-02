#!/usr/bin/env python

controller = dict(ip_add="127.0.0.1", serv_control_port="3000", client_control_port="8080")

'''
SERVER
ip_address of server to be passed as argument from terminal
controller_ip must be same as ip_add of controller
control_port must be same as serv_control_port of controller
no_of_conn is used to specify the number of clients that can connect to a single server
'''
server = dict(controller_ip="127.0.0.1", control_port="3000", command_port="5555", 
	data_port="2222", buffer_size="50", predictions="5",
	no_of_conn="10")

'''
CLIENT
controller_ip must be same as ip_add of controller
rrport must be same as client control port of controller
'''
client = dict(controller_ip="127.0.0.1", rrport="8080")