# base image
FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install locales

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
# set up environment for Python, ZeroMQ, OpenCV, and OpenALPR
RUN apt-get -y install apt-utils
RUN apt-get -yf install git build-essential cmake pkg-config wget
RUN apt-get -yf install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
RUN apt-get -yf install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get -yf install libxvidcore-dev libx264-dev
RUN apt-get -yf install libgtk2.0-dev
RUN apt-get -yf install libatlas-base-dev gfortran
RUN cd ~ && \
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
  apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev && \
  apt-get install -y tesseract-ocr libtesseract-dev && \
  apt-get install -y python-openalpr && \
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
