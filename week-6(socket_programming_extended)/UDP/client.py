import socket
from argparse import ArgumentParser

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--server-host', default="127.0.0.1")
    args.add_argument('--server-port', default=8000, type=int)
    return args.parse_args()

def start_udp_client(server_host, server_port):
    # create a client socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_DGRAM -> UDP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

        # send message to server at address (server_host, server_port)
        for message_id in range(1, 11):
            message = f"Ping #{message_id}".encode()
            client_socket.sendto(message, (server_host, server_port))


if __name__ == '__main__':
    args = parse_args()
    start_udp_client(args.server_host, args.server_port)