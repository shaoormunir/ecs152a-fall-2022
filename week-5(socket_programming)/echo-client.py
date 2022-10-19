# echo-client.py
import socket
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='python3 echo-client.py -p port -i host')
    parser.add_argument('-p', help='port_number', default=20000)
    parser.add_argument('-i', help='host_name', default='localhost')
    args = parser.parse_args()
    HOST = args.i
    PORT = int(args.p)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    print(f"Received {data.decode()!r} from {HOST}:{PORT}")