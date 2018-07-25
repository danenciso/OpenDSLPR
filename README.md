# OpenDSLPR
Open Distributed Streaming of License Plate Recognition. Provides scripts to manage image data transfer and frame-by-frame analytics of stored and live video feeds.

## What's new?
A new controller module is introduced. The controller authenticates the clients & servers and is supposed to manage the overall client/server network.\
The code uses zmq PUSH-PULL communication pattern for data transfer and zmq ROUTER-REP and REQ-REP patterns for control and command.\
Designed to be scalable and introduces commands and error codes.\
A *ClientConnectionRule* is introduced that can be used to dynamically control which clients are connected to which servers. The module can be easily expanded to add new rules./
Testing is done to a good extent.

## Terminology
A server JOINS a network, effectively after being authenticated by the controller, and it DISJOINS to leave the network.\
A client CONNECTS to the server(after authentication by controller) and DISCONNECTS from the server.

## Known Issues
None

## Controller
To be updated

## Server
To be updates

## Client
To be updated
