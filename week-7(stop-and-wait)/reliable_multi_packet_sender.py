import socket


def create_message(message_id, message):
    # return the message
    return f"#{message_id}: {message}"


# read alice29.txt file
with open("alice29.txt", "r") as file:
    message = file.read()


PKT_SIZE = 1000
WINDOW_SIZE = 6  # window size is 3 packets, so we can send 3 packets at a time and wait for 3 acknowledgements before sending the next 3 packets
packets = []

# split the message into packets
for i in range(0, len(message), PKT_SIZE):
    packets.append(message[i:i+PKT_SIZE])

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

    # bind the socket to a OS port
    udp_socket.bind(("localhost", 5000))

    # send the packets
    for i in range(0, len(packets), WINDOW_SIZE):
        # create the messages
        messages = []
        for j in range(WINDOW_SIZE):
            if i+j < len(packets):
                messages.append(create_message(i+j, packets[i+j]))

        # set timeout for 1 second
        udp_socket.settimeout(1)

        # send the messages
        for message in messages:
            udp_socket.sendto(message.encode(), ("localhost", 5001))

        # list to store the acknowledgements
        acknowledgements = [False for _ in range(WINDOW_SIZE)]

        # wait for acknowledgements
        while True:
            try:
                # receive the acknowledgement
                acknowledgement, _ = udp_socket.recvfrom(1024)

                # decode the acknowledgement
                acknowledgement = acknowledgement.decode()

                # get the message id
                message_id = int(acknowledgement.split('$')[0])

                # mark the acknowledgement as received
                acknowledgements[message_id - i] = True

                # print the acknowledgement
                print(acknowledgement)

                # check if all acknowledgements are received
                if all(acknowledgements):
                    break
            except socket.timeout:
                # if timeout occurs, resend the messages
                print(f"Timeout occured for #{i}, resending")
                for message in messages:
                    udp_socket.sendto(message.encode(), ("localhost", 5001))