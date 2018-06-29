FROM python:2.7.15
WORKDIR /usr/local/bin
COPY serverstart.py .
COPY sink.py .
COPY utils.py .
COPY recognition.py .
#Install modules
RUN pip install opencv-python pillow numpy pyzmq

ENV portnum="1111" ringbuff="1000" predict="5" numcon="1"
CMD python serverstart.py $portnum $ringbuff $predict $numcon
