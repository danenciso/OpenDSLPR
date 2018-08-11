#!/bin/bash

dslprversion="dfedock135/dslprserver:3.0"
port=$1
ringbuf=$2
predic=$3
numcon=$4

docker run -d -t -p $port:$port $dslprversion
dl="$(docker ps -l -q )"
docker exec -it $dl  sh -c "python ~/Server/servstart.py $port $ringbuf $predic $numcon"
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
