#!/usr/bin/env python3

from email import message
import sys
import socket
import selectors
import types
import argparse

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client", b"Message 2 from client"]


def start_connections(host, port, num_conns):
    # the server address tuple
    server_addr = (host, port)
    for i in range(0, num_conns):
        # for a given connection, we need to keep track of the connection id
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        # create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set the socket to non-blocking, so we can use the selector
        sock.setblocking(False)
        # connect to the server
        sock.connect_ex(server_addr)
        # types of events we are interested in
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # create a data object to store the connection id and the messages
        # add client id to the messages
        client_messages = [msg + b" " + str(connid).encode() for msg in messages]
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in client_messages),
            recv_total=0,
            messages=client_messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    # get the socket from the key
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # if we can read, it means the socket is ready to receive data
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            # if we have received all the data, we can close the connection
            print(f"Closing connection {data.connid}")
            # unregister the socket from the selector
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        # if we can write, it means the socket is ready to send data
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)
            # remove the sent data from the buffer
            data.outb = data.outb[sent:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='python3 multiconn-client.py -p port -i host -n num_conns')
    parser.add_argument('-p', help='port_number', default=20000)
    parser.add_argument('-i', help='host_name', default='localhost')
    parser.add_argument('-n', help='number_of_connections', default=1)
    args = parser.parse_args()
    HOST = args.i
    PORT = int(args.p)
    NUM_CONNS = int(args.n)

    # start the connections
    start_connections(HOST, PORT, NUM_CONNS)
    try:
        while True:
            # wait for an event to be ready
            events = sel.select(timeout=1)
            for key, mask in events:
                # print(f"Got event for {key.data.connid}")
                # for each event which is ready, call the service_connection function
                service_connection(key, mask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()