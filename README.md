# OpenDSLPR
Open Distributed Streaming of License Plate Recognition. Provides scripts to manage image data transfer and frame-by-frame analytics of stored and live video feeds.

## What's new?
A new controller module is introduced. The controller authenticates the clients & servers and is supposed to manage the overall client/server network.\
The code uses zmq PUSH-PULL communication pattern for data transfer and zmq REQ-REP pattern for control and command.\
Designed to be scalable and introduces commands and error codes.\
Basic testing is done.

## Terminology
A server JOINS a network, effectively after being authenticated by the controller, and it DISJOINS to leave the network.\
A client CONNECTS to the server(after authentication by controller) and DISCONNECTS from the server.

## Known Issues
The code is known to work **only** for **single client- single server** model. The *ManageServers* thread blocks after first server is joined, similarly, the *ManageClients* thread blocks after first client is connected.

## Controller
To be updated

## Server
To be updates

## Client
To be updated
