import socket
from argparse import ArgumentParser

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--host', default="127.0.0.1")
    args.add_argument('--port', default=8000, type=int)
    return args.parse_args()

def start_udp_server(host, port):
    # create a server socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_DGRAM -> UDP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

        # bind the socket to a OS port
        server_socket.bind((host, port))

        # start receiving udp packets in an infinite loop
        while True:
            # data, addr = recvfrom(n)
            #   n -> buffer size, i.e., number of max bytes to receive
            #   data -> the message received from the client
            #   addr -> the address of the client
            message, addr = server_socket.recvfrom(1024)

            # decode the message and print
            print(f"Message from {addr}: {message.decode()}")


if __name__ == '__main__':
    args = parse_args()
    start_udp_server(args.host, args.port)