#!/usr/bin/python3.5
'''
CODE  = identifier sent in the previouse step
Step 1: UDP
-----------

- Create a UDP server on your machine (on the port you want)
- Send a message to the UDP server atclab.esi.uclm.es: 2000
  indicating the identifier "CODE" and the port on which you have created
  your UDP server, separated by a space.
  Example: "CODE 7777" (without quotes).

Your UDP server will receive the instructions to continue.
You have 4 seconds.

Hints:
- Check that it is possible to connect to your UDP server from a machine with
  a public IP (use netcat to check that).

'''

import socket as s

port = 2000
host = "atclab.esi.uclm.es"


# The function creating a server UDP that send a message and
# receive a message with next port
# @input: port(string)
# @output port(string)
def init(code):
    print("\n------------------STEP 1------------------\n")
    print("Creating socket...")
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    print("done.")

    # binding the server
    sock.bind(('', 12345))

    # creating string to send to the host
    data = "{} 12345".format(code)
    print("Send data " + data)
    sock.sendto(data.encode(), (host, port))
    print("Done")

    print("Receiving message from other server...")
    msg, master = sock.recvfrom(1024)
    print("Message is arrived")

    # Creating a file to store the instructions
    f = open("inst_step2.txt", "w")
    f.write(msg.decode())
    f.close()
    sock.close()

    # The first line of the message contain the next port
    return msg.decode().partition("\n")[0]
