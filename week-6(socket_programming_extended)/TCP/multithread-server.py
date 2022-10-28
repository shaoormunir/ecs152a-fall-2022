import socket
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--host', default="127.0.0.1")
    args.add_argument('--port', default=8000, type=int)
    return args.parse_args()

def client_handler(socket, addr, client_id):
    # communicate with client until it disconnects
    message_id = 1
    while True:
        print(f"New client {addr} connected!")

        # data = recv(n)
        #   n -> buffer size, i.e., number of max bytes to receive
        #   data -> the message received from the client
        
        message = socket.recv(1024)

        if message:
            # decode the message and print
            print(f"Message from {addr}: {message.decode()}")

            # delay for client_id 1
            if client_id == 1:
                sleep(5)
                pass

            # send response
            message = socket.sendall(f"Pong #{message_id}".encode())
            message_id += 1
        else:
            # on empty message, client has exited
            socket.close()
            break
 
def start_multithreaded_tcp_server(host, port):
    # create a server socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_STREAM -> TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket to a OS port
        server_socket.bind((host, port))

        # start listening for connections
        server_socket.listen()

        # client ids
        client_id = 0

        # create a processing pool for threads with max number of threads as 5
        with ThreadPoolExecutor(max_workers=5) as executor:

            # start accepting tcp connections in a loop
            while True:
                # wait for a new connection
                #   client_socket -> send/recv data from client
                #   client_addr -> (ip, port) of client
                client_socket, client_addr = server_socket.accept()

                # start a new thread with client_handler method as entrypoint and 
                # client_socket, client_addr as parameters
                # i.e.,
                # the thread will start in the client_handler function and the values
                # of client_socket and client_addr will be passed to that thread
                executor.submit(client_handler, client_socket, client_addr, client_id)
                
                # increment client id
                client_id += 1

            


if __name__ == '__main__':
    # parse command line arguments
    args = parse_args()

    # start the tcp server
    start_multithreaded_tcp_server(args.host, args.port)