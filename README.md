# OpenDSLPR
Open Distributed Streaming of License Plate Recognition. Provides scripts to manage image data transfer and frame-by-frame analytics of stored and live video feeds.

Works via Client and Server distribution. Client operates as endpoint to send frames to Server. Server utilizes the open-source [OpenALPR](https://github.com/openalpr/openalpr) library for Automatic License Plate Recognition. 

Must be in same subnet for correct functionality (i.e. client to know server). Can be accomplished using [IPoP](https://github.com/ipop-project), an open-source user-centric software virtual network.

#### Coming soon
**Message queue** to be enabled by [ZeroMQ](https://github.com/zeromq) for distributed messaging and queue management.

**Container portability** via Docker images of OpenDSLPR Server & Client for simplified setup and tesing.


## Client
Python script receives video and sends to an IP address and port acting as the server.

Exits when message has been sent.

## Server
Kept alive and is open to receive frames from Client sender. Python scripts initialize server instance and include dependencies for lincense plate recognition.
 
