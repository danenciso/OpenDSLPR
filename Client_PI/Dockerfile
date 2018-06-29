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
  apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev && \
  apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev && \
  apt-get install libxvidcore-dev libx264-dev && \
  apt-get install libgtk2.0-dev && \
  apt-get install libatlas-base-dev gfortran && \
  cd ~ && \
  git clone https://github.com/opencv/opencv.git && \
  cd opencv && \
  git checkout 3.4 &&\
  cd ~ && \
  git clone https://github.com/opencv/opencv_contrib.git && \
  cd opencv_contrib &&\
  git checkout 3.4 && \
  cd / && \
  apt-get install -y python2.7 && \
  wget https://bootstrap/pypa.io/get-pip.py && \
  python get-pip.py && \
  pip install numpy && \
  pip install pyzmq && \
  pip install pillow  && \ 
  cd ~/opencv  && \
  mkdir build && \
  cd build && \
  cmake -D CMAKE_BUILD_TYPE=RELEASE, -D CMAKE_INSTALL_PREFIX=/usr/local, -D INSTALL_C_EXAMPLES=OFF, -D INSTALL_PYTHON_EXAMPLES=ON, -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules, -D BUILD_EXAMPLES=ON && \
  make && \
  make install && \
  ldconfig && \
  rm -rf /var/lib/apt/lists/*


# Now include the application-specific
WORKDIR /usr/local/bin
COPY client.py .
COPY v.mp4 .

ENV serverad="10.0.0.0" portnum="1111" videofile="v.mp4"

CMD python client.py $serverad $portnum $videofile
