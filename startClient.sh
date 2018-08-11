#!/bin/bash

dslprversion="dfedock135/rpi-dslprclient:3.0"

serverad=$1
port=$2
video=$3
docker run -d -t $dslprversion bash
dl="$(docker ps -l -q )"
docker cp $video $dl:/usr/local/bin
docker exec -it $dl sh -c "python client.py $serverad $port $video"
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
