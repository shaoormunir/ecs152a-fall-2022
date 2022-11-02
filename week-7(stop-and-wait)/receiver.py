import random
import socket

def create_acknowledgement(message_id):
    # return the acknowledgement
    return f"{message_id}$ Acknowledged"

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    # bind the socket to a OS port
    udp_socket.bind(("localhost", 5001))

    # start receiving packets
    while True:
        # receive the packet
        packet, _ = udp_socket.recvfrom(1024)

        # decode the packet
        packet = packet.decode()

        # get the message id
        message_id = int(packet.split(":")[0][1:])

        # randomly drop the packet
        random_chance = random.randint(0, 100)
        if random_chance < 50:
            print(f"Packet #{message_id} dropped")
            continue

        # create the acknowledgement
        acknowledgement = create_acknowledgement(message_id)

        # send the acknowledgement
        udp_socket.sendto(acknowledgement.encode(), ("localhost", 5000))

        # print the packet
        print(packet)