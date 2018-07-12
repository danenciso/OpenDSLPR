import sink, sys, thread, threading, utils

if __name__ == '__main__':
	if len(sys.argv) != 9:
		print("Usage : python <script_name> <IP-address> <Controller-IP> <Control-Port> <Command-port> <Data-Port> <Size_of_Ring_Buffer> <Predictions> <No_of_Connections> ")
		sys.exit()

	servconfig = sink.Config() 		#intitialize port, number of clients, buffer size, etc
	#print("Connected to client")

	#Command-port starts listening for commands from controller in future
	thread0 = threading.Thread(name="Listen_Controller", target=utils.Control._scan, args=(servconfig,))
	thread0.start()

	#Send JOIN! request to controller
	utils.Control._join(servconfig)

	get = sink.ReceiveFrames()
	put = sink.AlprProcessing()
	manage = utils.ManageClients()
	
	thread1 = threading.Thread(name="Add_Client", target=manage._scan, args=(servconfig,))
	thread2 = threading.Thread(name="Get_Frames", target= get._get_stream, args=(servconfig,))
	thread3 = threading.Thread(name="Process_Frames", target= put._put_alpr, args=(servconfig,))
	thread1.start()
	thread2.start()
	thread3.start()