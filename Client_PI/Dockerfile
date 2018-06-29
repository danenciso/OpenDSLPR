# base image
FROM ubuntu:16.04

# minimal install above requires additional work
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  rpi-update && \
  reboot && \
  apt-get install wget cmake build-essential git pkg-config && \
  apt-get install -y python2.7 && \
  wget https://bootstrap/pypa.io/get-pip.py && \
  python get-pip.py && \
  pip install numpy  
  cd ~/opencv  && \
  
  rm -rf /var/lib/apt/lists/*


# Now include the application-specific
WORKDIR /usr/local/bin
COPY client.py .
COPY v.mp4 .

ENV serverad="10.0.0.0" portnum="1111" videofile="v.mp4"

CMD python
