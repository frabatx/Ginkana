#!/usr/bin/python3.5
'''
The program create a soket that can connect with
host: atclab.esi.uclm.es
port: 2000
Stamp a message that contain the next port to next step.
'''
import socket as s

port = 2000
host = "atclab.esi.uclm.es"


# The function create a socket and return a string using socket module
# @input: None
# @output: port(string)
def init():
    print("\n------------------STEP 0------------------\n")

    print("Creating socket...")
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    print("Done")
    print("Done")

    print("Connecting to remote host on port %d..." % port)
    sock.connect((host, port))
    print("Done")

    print("Receiving message from the host: {}".format(host))
    msg, client = sock.recvfrom(1024)
    print("Done")

    # Creating a file to store the instructions
    f = open("inst_step1.txt", "w")
    f.write(msg.decode())
    f.close()
    sock.close
    # The first line of the message contain the next port
    return msg.decode().partition("\n")[0]
