import sink, sys, thread, threading

if __name__ == '__main__':
	if len(sys.argv) != 7:
		print("Usage : python <script_name> <No_of_Connections> <Port> <Size_of_Ring_Buffer> <Predictions> <framerate_port> <frame_interval>")
		sys.exit()

	bind, get, put, push = sink.Connection(), sink.ReceiveFrames(), sink.AlprProcessing(), sink.FrameRateUpdateService()
	bind._connect()

	thread0 = threading.Thread(name="Connection", target=bind._disconnect)
	thread1 = threading.Thread(name="Get_Frames_Stream_from_cam", target=get._get_stream)
	thread2 = threading.Thread(name="Put_Frame_Stream_for_recogniztion", target=put._put_alpr)
	thread3 = threading.Thread(name="Frame_rate_update_server", target=push._send_update)
	thread0.start()
	thread1.start()
	thread2.start()
	thread3.start()
