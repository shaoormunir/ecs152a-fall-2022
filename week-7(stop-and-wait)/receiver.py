import random
import socket

def create_acknowledgement(message_id):
    # return the acknowledgement
    return f"{message_id}$ Acknowledged"


# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    # bind the socket to a OS port
    udp_socket.bind(("localhost", 5001))

    data_buffer = {}
    # start receiving packets
    while True:
        timeouts = 0
        try:
            # receive the packet
            packet, _ = udp_socket.recvfrom(2048)

            # decode the packet
            packet = packet.decode()

            # get the message id
            message_id = int(packet.split("@")[0][1:])

            # if the message id is -1, we have received all the packets
            if message_id == -1:
                # send the acknowledgement
                udp_socket.sendto(create_acknowledgement(message_id).encode(), ("localhost", 5000))
                break

            # get the message
            message = packet.split("@")[1][1:]

            # randomly drop the packet
            random_chance = random.randint(0, 100)
            if random_chance < 10:
                print(f"Packet #{message_id} dropped")
                continue

            # Printing the message to the console.
            # print(message)
            # add the message to the buffer
            data_buffer[message_id] = message

            # create the acknowledgement
            acknowledgement = create_acknowledgement(message_id)

            # send the acknowledgement
            udp_socket.sendto(acknowledgement.encode(), ("localhost", 5000))
        except socket.timeout:
            timeouts += 1
            if timeouts > 3:
                break
    
    # reconstruct the message using the buffer
    message = ""
    sorted_data = sorted(data_buffer.items())

    print(sorted_data)

    for data in sorted_data:
        message += data[1]
    
    print(message)