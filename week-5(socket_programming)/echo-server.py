import socket
import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='python3 echo-server.py -p port -i host')
    parser.add_argument('-p', help='port_number', default=20000)
    parser.add_argument('-i', help='host_name', default='localhost')

    args = parser.parse_args()

    HOST = args.i
    PORT = int(args.p)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            print(f"Listening on {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received {data.decode()!r} from {addr}")
                conn.send(data)
                time.sleep(10)