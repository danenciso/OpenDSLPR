FROM dfedock135/cvpymqpr:1.0
WORKDIR /usr/local/bin
COPY servstart.py .
COPY sink.py .
COPY utils.py .
COPY recognition.py .

ENV portnum="1111" ringbuff="1000" predict="5" numcon="1"
CMD python servstart.py $portnum $ringbuff $predict $numcon
