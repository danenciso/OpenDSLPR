FROM python:2.7.15
WORKDIR /usr/local/bin
COPY client.py .
COPY v.mp4 .
#Install modules
RUN pip install opencv-python pillow numpy pyzmq 

ENV serverad="10.0.0.0" portnum="1111" videofile="v.mp4"

CMD python client.py $serverad $portnum $videofile
