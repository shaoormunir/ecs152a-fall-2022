import socket

def create_message(message_id, message):
    # return the message
    return f"#{message_id}: {message}"


# read alice29.txt file
with open("alice29.txt", "r") as file:
    message = file.read()


PKT_SIZE = 1000
packets = []

# create packets using create message function
for i in range(0, len(message), PKT_SIZE):
    packets.append(create_message(i//PKT_SIZE, message[i:i+PKT_SIZE]))

# append the last message with message id -1
packets.append(create_message(-1, ""))

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

    # bind the socket to a OS port
    udp_socket.bind(("localhost", 5000))
    i = 0
    # send the packets
    for message in packets:
        try:
            # set timeout for 1 second
            udp_socket.settimeout(1)

            # send the message
            udp_socket.sendto(message.encode(), ("localhost", 5001))

            # wait for acknowledgement

            # receive the acknowledgement
            acknowledgement, _ = udp_socket.recvfrom(1024)

            # decode the acknowledgement
            acknowledgement = acknowledgement.decode()

            # because we are unreliable, we are dropping it
        except socket.timeout:
            # if timeout occurs, resend the message
            print(f"Timeout occured for #{i}, we don't care. We are unreliable")
        
        i += 1