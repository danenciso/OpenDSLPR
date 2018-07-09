# base image
FROM resin/rpi-raspbian
ENTRYPOINT []

# set up environment for Python, ZeroMQ, and OpenCV
RUN \
  apt-get update && \
  apt-get -y install apt-utils && \
  apt-get -y install wget cmake build-essential git pkg-config && \
  apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev && \
  apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev && \
  apt-get -y install libxvidcore-dev libx264-dev && \
  apt-get -y install libgtk2.0-dev && \
  apt-get -y install libatlas-base-dev gfortran && \
  cd ~ && \
  git clone https://github.com/opencv/opencv.git && \
  cd opencv && \
  git checkout 3.4 &&\
  cd ~ && \
  git clone https://github.com/opencv/opencv_contrib.git && \
  cd opencv_contrib &&\
  git checkout 3.4 && \
  cd / && \
  apt-get -y install python-dev && \
  apt-get -y install python-numpy && \
  apt-get -y install python-pil && \
  apt-get -y install libzmq3-dev && \
  wget https://bootstrap.pypa.io/get-pip.py && \
  python get-pip.py && \
  pip install pyzmq && \
  cd ~/opencv  && \
  mkdir build && \
  cd build && \
  cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D BUILD_EXAMPLES=ON .. && \
  make && \
  make install && \
  ldconfig && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf ~/opencv*

