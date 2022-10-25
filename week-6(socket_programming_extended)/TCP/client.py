import socket
from argparse import ArgumentParser
from time import sleep
from concurrent.futures import ThreadPoolExecutor

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--server-host', default="127.0.0.1")
    args.add_argument('--server-port', default=8000, type=int)
    args.add_argument('--num-clients', default=1, type=int)
    return args.parse_args()

def start_tcp_client(client_id, server_host, server_port):
    # create a client socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_STREAM -> TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # connect to TCP server
        client_socket.connect((server_host, server_port))

        # send message to TCP server at address (server_host, server_port)
        for message_id in range(1, 11):
            # send message to server
            message = f"Ping #{message_id}".encode()
            client_socket.sendall(message)

            # get reply from server
            reply = client_socket.recv(1024)
            print(f"Client #{client_id}: Message from server:", reply.decode())

            sleep(0.1)


if __name__ == '__main__':
    # parse command line arguments
    args = parse_args()

    # create multiple clients in different threads
    with ThreadPoolExecutor(max_workers=args.num_clients) as executor:
        for client_id in range(args.num_clients):
            executor.submit(start_tcp_client, client_id, args.server_host, args.server_port)