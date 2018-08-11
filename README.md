# OpenDSLPR
Open Distributed Streaming of License Plate Recognition. Provides scripts to manage image data transfer and frame-by-frame analytics of stored and live video feeds.

Works via Client and Server distribution. Client operates as endpoint to send frames to Server. Server utilizes the open-source [OpenALPR](https://github.com/openalpr/openalpr) library for Automatic License Plate Recognition. 

Must be in same subnet for correct functionality (i.e. client to know server). Can be accomplished using [IPoP](https://github.com/ipop-project), an open-source user-centric software virtual network.

### Unique Features
**Message queue** to be enabled by [ZeroMQ](https://github.com/zeromq) for distributed messaging and queue management.

**Container portability** via Docker images of OpenDSLPR Server & Client for simplified setup and tesing. Currently available for client.

## Client
Python script receives video and sends to an IP address and port acting as the server. User is required to set destination IP address and port number as well as the video file that they are passing.

Exits when message has been sent.

A Docker Image is now publicly available. If you have a Docker Hub account and Docker installed on your host machine, the command to grab the image is **dfedock135/dslprclient**

To run the client: **docker run --env serverad=XXX.XXX.XXX.XXX --env portnum XXXX --env videofile=path/somevideo dfedocke135/dslprclient:1.0**

The startClient.sh script is intended for the Raspbian Docker Image and should only be run for clients for that context. The script can be modified to work for Docker for other processors, it is just a matter of correcting the image that is referred to in the script.

## Server
Kept alive and is open to receive frames from Client sender. Python scripts initialize server instance and include dependencies for lincense plate recognition.

The startServer.sh will work for Docker on Ubuntu, Mac, and Windows.
 
