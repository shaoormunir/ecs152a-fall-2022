#!/usr/bin/env python3
import socket
import selectors
import types
import argparse
import time

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    # Accept a connection and register the socket with the selector
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    # Set the socket to non-blocking
    conn.setblocking(False)
    # Create a data object to store the connection id and the messages
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # Register the socket with the selector
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    # Get the socket from the key
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # If we can read, it means the socket is ready to receive data
        recv_data = sock.recv(1024)
        if recv_data:
            # If we have received data, store it in the data object
            data.outb += recv_data
        else:
            # If we have received no data, it means the connection is closed
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        # If we can write, it means the socket is ready to send data
        if data.outb:
            # If we have data to send, send it
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="python3 multiconn-server.py -p port -i host -n num_conns")
    parser.add_argument("-p", help="port_number", default=20000)
    parser.add_argument("-i", help="host_name", default="localhost")
    parser.add_argument("-n", help="number_of_connections", default=1)

    args = parser.parse_args()

    HOST = args.i
    PORT = int(args.p)
    NUM_CONNS = int(args.n)

    # create a TCP socket
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the socket to non-blocking, so we can use the selector
    lsock.bind((HOST, PORT))
    lsock.listen(NUM_CONNS)
    print(f"Listening on {HOST}:{PORT}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            # wait for events
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    # if the key has no data, it means it is a new connection
                    accept_wrapper(key.fileobj)
                else:
                    # otherwise, it is an existing connection
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()