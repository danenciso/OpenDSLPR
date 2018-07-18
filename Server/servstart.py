import sink, sys, time, thread, threading, utils

if __name__ == '__main__':
	if len(sys.argv) != 9:
		print("Usage : python <script_name> <IP-address> <Controller-IP> <Control-Port> <Command-port> <Data-Port> <Size_of_Ring_Buffer> <Predictions> <No_of_Connections> ")
		sys.exit()

	do_exit = False
	servconfig = sink.Config() 		#intitialize port, number of clients, buffer size, etc
	#print("Connected to client")

	#Command-port starts listening for any commands from controller in future
	#Spawns thread internally when constructor is called
	Scanner = utils.Scan(servconfig)

	#Send JOIN! request to controller
	utils.Control._join(servconfig)

	get = sink.ReceiveFrames()
	put = sink.AlprProcessing()
	
	thread2 = threading.Thread(name="Get_Frames", target= get._get_stream, args=(servconfig,))
	thread3 = threading.Thread(name="Process_Frames", target= put._put_alpr, args=(servconfig,))
	thread2.start()
	thread3.start()

	
	while do_exit==False:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			do_exit = True

	Scanner.stop()
	servconfig.command.close()
	servconfig.receiver.close()