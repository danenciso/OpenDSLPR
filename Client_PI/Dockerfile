FROM dfedock135/rpi-cvpymq:1.0
# Now include the application-specific
WORKDIR /usr/local/bin
COPY client.py .
COPY v.mp4 .

ENV serverad="10.0.0.0" portnum="1111" videofile="v.mp4"

CMD python client.py $serverad $portnum $videofile
