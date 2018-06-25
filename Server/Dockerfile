FROM python:2.7.15
WORKDIR /usr/local/bin
COPY main.py .
COPY 
#Install modules
RUN pip install opencv-python pillow numpy

ENV portnum="1111" videofile="v.mp4"
CMD ["python","send.py","portnum","videofile"]

