# TCP Sockets
## Description
In TCP, there is an established connection between the client and the server. The server calls the `listen()` method to start accepting new connections. The client calls the ``connect()`` method to connect to the server. This repository contains three different server implementations which incrementally build on top of one another. We walk over these increments in [Server Types](#server-types).

## Usage
### Starting the Server
To start the server, run ```python TCP/server.py``` which will bind and listen on host `127.0.0.1` and port `8000` by default. You can change these by setting the `--host` and `--port` arguments from the command-line.

### Starting the Clients
To start the clients, run ```python TCP/client.py``` which will create a single-client by default that establishes a TCP connection to host `127.0.0.1` and port `8000` by default. To create several different parallel clients, pass the `--num-clients` argument with the number of clients.

## <a name="server-types"></a>Server Types
### Simple TCP Server
The simple TCP server implements a single-threaded TCP server that sequentially listens for new connections, connects to the client, receives messages and sends responses until the client leaves, and then waits for a new connection. Run this using `python TCP/server.py`.

This server is severely limited because it can only treat with one client at a time. To test this, run the client using `python TCP/client.py --num-clients 5` which runs 5 clients in parallel. On the client-side terminal, you will see that the responses for the clients are sequential, i.e., Client #0 receives the 10 pongs first before Client #1 receives it and so on. Similarly, on the server-side terminal you will see that the new client message only prints after the previous client has disconnected.

### Multi-Select TCP Server
The first incremental update we make to the simple TCP server is to set it to non-blocking mode. This is accomplished by using the `setblocking(False)`  method on the socket which prevents `accept()`, `recv()`, and `send()` from blocking the program. Run this using `python TCP/multiselect-server.py`.

This server provides the ability to deal with multiple clients by preventing the program from being blocked when one client is waiting to send/receive data or a new client is trying to connect. To test this, run the client using `python TCP/client.py --num-clients 5` which runs 5 clients in parallel. You will see that all clients are able to connect to the server concurrently and the server responds to them concurrently as well. Look at the client-side terminal and you'll see that the Client #'s are all out of order and the program finishes almost instanteneously.

The code for the multi-select TCP server is fairly complicated but the main gist of it is that you're setting the sockets to non-blocking so they don't block the program and only focusing on sockets that have something to read/write or the server socket when it is accepting a new connection.

### Multi-Threaded TCP Server
The second incremental update we make to the simple TCP server is to use threads instead of multi-select. While the multi-select server is capable of handling multiple clients, it is still effectively running one program thread. This would work for a simple ping-pong server but suppose the server has to run a time-consuming computation or perform some CPU intensive tasks. In that case, it won't be able to respond to the clients quick enough.

To illustrate this, open the `multiselect-server.py` file and uncomment line #118. This line causes the program to sleep for 5 seconds before sending the response for client #1 simulating the scenario where one particular client needs the server to perform a long-running operation. You can see in the client-side terminal that no other client receives a response while the server is performing this operation. This can be resolved by using threads.

All programs have one thread by default called the main thread. The main thread is where the main flow of the program executes. A program can create several threads that can be assigned to different CPUs and/or cores to speed up the program execution. These different threads can be executed concurrently and then merged with the main program. This works well when the tasks are independent of each other. In the client-server architecture, clients generally act independently of other clients so multi-threading can help fasten the server.

The core principle is that every new client is assigned a new thread. The more powerful the machine, the more threads that can be made, and hence the more clients can connect. The multi-threaded implementation can be run using `python TCP/multithread-server.py`. Again, run the server and then create several clients using `python TCP/client.py --num-clients 5`. You will see that the clients are concurrently run like before but this time they run in different threads. You could have the threads sleep for some duration using `time.sleep()` and that would not impact the other clients as it would've in the multi-select TCP server. To demonstrate this, open `multithread-server.py` and uncomment line #31. This line causes the program to sleep for 5 seconds before sending the response for client #1. This time, compared to `multiselect-server.py`, you will see that the responses for client #1 arrive in 5 second delays but the other clients are not effected because only the thread handling that particular client is put to sleep.

Multithreading in Python can be performed using several libraries, e.g., `threading`, `multiprocessing`, `concurrent.futures`. The provided sample code uses `concurrent.futures.ThreadPoolExecutor` to create multiple threads. This class provides a pool to which different threads can be submitted along with a maximum number of concurrent threads to prevent overloading the server. The `submit()` function takes the name of a thread entrypoint function along with the parameters for that function.