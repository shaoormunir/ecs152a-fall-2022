# UDP Sockets
## Description
In UDP, there is no agreed upon connection between the client and the server. The client sends a message to the UDP server without establishing a connection and does not receiving any acknowledgment of receipt from the server. As such, there is no need for the server to call the `listen()` method as it is not accepting connections but rather just packets.

## Usage
### Starting the Server
To start the server, run ```python UDP/server.py``` which will bind on host `127.0.0.1` and port `8000` by default. You can change these by setting the `--host` and `--port` arguments from the command-line.

### Starting the Clients
To start the clients, run ```python UDP/client.py``` which will send UDP Packets to host `127.0.0.1` and port `8000` by default. You should see these printed on the server-side terminal.

