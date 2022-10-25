import socket
from argparse import ArgumentParser
import select
from time import sleep

# struct for storing client state
class Client:
    def __init__(self, addr, client_id):
        self.addr = addr
        self.client_id = client_id
        self.hasPinged = False
        self.pongCount = 1


def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--host', default="127.0.0.1")
    args.add_argument('--port', default=8000, type=int)
    return args.parse_args()

def start_multi_tcp_server(host, port):
    # create a server socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_STREAM -> TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket to a OS port
        server_socket.bind((host, port))

        # start listening for connections
        server_socket.listen()

        # set socket as non-blocking so calls dont block forever
        server_socket.setblocking(False)

        # configure sources of input and output
        #   server_socket input means a new connection
        inputs = [server_socket]
        # we will populate outputs as new clients connect
        outputs = []

        # create a list of client connections to keep track of their data
        clients = {}
        client_id = 0

        # while we still have inputs to read from
        while inputs:

            # select.select(param1, param2, param3, timeout) takes three parameters and returns three lists
            #   param1 -> file descriptors we can read from (e.g., server sockets, client sockets)
            #   param2 -> file descriptors we can write to (e.g., client sockets)
            #   param3 -> file descriptors that can throw exceptions (e.g., client sockets on disconnect)
            #   timeout -> timeout for non-block
            # The return values are sub-lists of the three parameters that contain 
            # the file descriptors that are ready for the corresponding operation
            # readables is a sub-list of param1 (inputs) that contains sockets that are ready for reading
            # writables is a sub-list of param2 (outputs) that contains sockets that are ready for writing
            # exceptionals is a sub-list of param3 (inputs) that contains sockets that have errored out
            readables, writables, exceptionals = select.select(inputs, outputs, inputs, 1)


            # iterate over readable sockets and handle accordingly
            for sock in readables:
                # if the socket is the server_socket and is readable, it is accepting new connections
                if sock is server_socket:
                    # accept the new connection, you can also use server_socket.accept()
                    client_socket, client_addr = sock.accept()

                    # set socket as non blocking too
                    client_socket.setblocking(False)

                    # once client connects, add them to the list of inputs and outputs
                    inputs.append(client_socket)
                    outputs.append(client_socket)

                    # create a dictionary so we can access this client later
                    clients[client_socket] = Client(client_addr, client_id)

                    # increment client id
                    client_id += 1

                    print(f"New client {client_addr} connected!")

                else:
                    # if socket is not server_socket, it is a client socket sending some data

                    # get client from clients dictionary
                    client = clients[sock]

                    # receive message from client
                    message = sock.recv(1024)
                    message = message.decode()

                    # set client ping to True so we can respond
                    if message and "Ping" in message:
                        # print message from client
                        print(f"Message from {client.addr}: {message}")
                        client.hasPinged = True
                    else:
                        # if empty message, disconnect client
                        inputs.remove(sock)
                        outputs.remove(sock)
                        sock.close()


            # iterate over writable sockets and handle
            for sock in writables:
                # writables will always be a client socket

                # get client from clients dictionary
                client = clients[sock]

                # check if client has pinged and is expecting a pong
                if client.hasPinged:
                    # add a delay before sending response
                    if client.client_id == 1:
                        # sleep(5)
                        pass
                    # send pong
                    sock.sendall(f"Pong #{client.pongCount}".encode())
                    # increment count of pong
                    client.pongCount += 1
                    # set hasPinged to False
                    client.hasPinged = False


            # iterate over exception sockets and handle
            for sock in exceptionals:
                inputs.remove(sock)
                outputs.remove(sock)
                del clients[sock]
                sock.close()




if __name__ == '__main__':
    # parse command line arguments
    args = parse_args()

    # start the tcp server
    start_multi_tcp_server(args.host, args.port)