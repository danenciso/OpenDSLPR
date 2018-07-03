# base image
FROM ubuntu:16.04

# minimal install above requires additional work

#  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \

RUN \
  apt-get update && \
  apt-get install -y apt-utils && \
  apt-get install -y wget cmake build-essential git pkg-config && \
  apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev && \
  apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev && \
  apt-get install -y libxvidcore-dev libx264-dev && \
  apt-get install -y libgtk2.0-dev && \
  apt-get install -y libatlas-base-dev gfortran && \
  cd ~ && \
  git clone https://github.com/opencv/opencv.git && \
  cd opencv && \
  git checkout 3.4 &&\
  cd ~ && \
  git clone https://github.com/opencv/opencv_contrib.git && \
  cd opencv_contrib &&\
  git checkout 3.4 && \
  cd / && \
  apt-get install -y python-dev && \
  apt-get install -y python-numpy && \
  apt-get install -y python-pil && \
  apt-get install -y libzmq3-dev && \
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
  rm -rf /var/lib/apt/lists/*


# Now include the application-specific
WORKDIR /usr/local/bin
COPY client.py .
COPY v.mp4 .

ENV serverad="10.0.0.0" portnum="1111" videofile="v.mp4"

CMD python client.py $serverad $portnum $videofile
