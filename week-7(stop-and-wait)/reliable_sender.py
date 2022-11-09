import socket


def create_message(message_id, message):
    print(message)
    print(message_id)
    # return the message
    return f"#{message_id}@ {message}"


# read alice29.txt file
with open("alice29.txt", "r") as file:
    message = file.read()


PKT_SIZE = 1000
packets = []

j = 0
i = 0
# create packets using create message function, also handle the case when the message is not a multiple of PKT_SIZE, and the last part of the message might not be added to the packets list
while i < len(message):
    if i + PKT_SIZE < len(message):
        packets.append(create_message(j, message[i:i+PKT_SIZE]))
        i += PKT_SIZE
        j += 1
    else:
        packets.append(create_message(j, message[i:]))
        i += PKT_SIZE
        j += 1

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

    # bind the socket to a OS port
    udp_socket.bind(("localhost", 5000))

    # send the packets
    i = 0
    for message in packets:
        # set timeout for 1 second
        udp_socket.settimeout(1)

        # send the message
        udp_socket.sendto(message.encode(), ("localhost", 5001))

        # wait for acknowledgement
        while True:
            try:
                # receive the acknowledgement
                acknowledgement, _ = udp_socket.recvfrom(1024)

                # decode the acknowledgement
                acknowledgement = acknowledgement.decode()

                # check if the acknowledgement is correct
                if acknowledgement == f"{i}$ Acknowledged":
                    # print the acknowledgement
                    print(acknowledgement)
                    break
            except socket.timeout:
                # if timeout occurs, resend the message
                print(f"Timeout occured for #{i}, resending")
                udp_socket.sendto(message.encode(), ("localhost", 5001))
        i += 1
    
    # send the last message with message id -1
    udp_socket.sendto(create_message(-1, "").encode(), ("localhost", 5001))
