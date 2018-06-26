import sink, sys, thread, threading, utils

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Usage : python <script_name> <Port> <Size_of_Ring_Buffer> <Predictions> <No_of_Connections> ")
		sys.exit()

	servconfig = utils.Config() 		#intitialize port, number of clients, buffer size, etc
	get = sink.ReceiveFrames()
	put = sink.AlprProcessing()
	#thread0 = threading.Thread(name="Connection", target=bind._disconnect)

	thread1 = threading.Thread(name="Get_Frames", target= get._get_stream, args=(servconfig,))
	thread2 = threading.Thread(name="Process_Frames", target= put._put_alpr, args=(servconfig,))
	#thread0.start()
	thread1.start()
	thread2.start()