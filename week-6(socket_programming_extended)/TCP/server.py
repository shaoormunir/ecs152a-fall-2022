import socket
from argparse import ArgumentParser

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--host', default="127.0.0.1")
    args.add_argument('--port', default=8000, type=int)
    return args.parse_args()

def start_tcp_server(host, port):
    # create a server socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_STREAM -> UDP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket to a OS port
        server_socket.bind((host, port))

        # start listening for connections
        server_socket.listen()

        # start accepting tcp connections in a loop
        while True:
            # wait for a new connection
            #   client_socket -> send/recv data from client
            #   client_addr -> (ip, port) of client
            client_socket, client_addr = server_socket.accept()

            print(f"\nNew client {client_addr} connected!")
            # communicate with client until it disconnects
            message_id = 1
            while True:
                # data = recv(n)
                #   n -> buffer size, i.e., number of max bytes to receive
                #   data -> the message received from the client
                
                message = client_socket.recv(1024)

                if message:
                    # decode the message and print
                    print(f"Message from {client_addr}: {message.decode()}")

                    # send response
                    message = client_socket.sendall(f"Pong #{message_id}".encode())
                    message_id += 1
                else:
                    # on empty message, client has exited
                    print(f"Client {client_addr} disconnected!")
                    client_socket.close()
                    break

                


if __name__ == '__main__':
    # parse command line arguments
    args = parse_args()

    # start the tcp server
    start_tcp_server(args.host, args.port)