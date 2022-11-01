import socket

def create_message(message_id, message):
    # return the message
    return f"#{message_id}: {message}"



# read alice29.txt file
with open("alice29.txt", "r") as file:
    message = file.read()


PKT_SIZE = 1000
packets = []

# split the message into packets
for i in range(0, len(message), PKT_SIZE):
    packets.append(message[i:i+PKT_SIZE])

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
  
      # bind the socket to a OS port
      udp_socket.bind(("localhost", 5000))

      # send the packets
      for i in range(len(packets)):
          # create the message
          message = create_message(i, packets[i])

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
                  if acknowledgement == f"#{i} Acknowledged":
                      # print the acknowledgement
                      print(acknowledgement)
                      break
              except socket.timeout:
                  # if timeout occurs, resend the message
                  print(f"Timeout occured for #{i}, resending")
                  udp_socket.sendto(message.encode(), ("localhost", 5001))