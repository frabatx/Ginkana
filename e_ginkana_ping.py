#!/usr/bin/python3

import socket
import struct
import time
import random

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')
DEST = "atclab.esi.uclm.es"


def init(data):
    print("STEP 4--------------------")
    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)

    # create a packet without checksum
    pack_id = int((id(1) * random.random()) % 65535)
    pack_sq_number = 1
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, pack_id, pack_sq_number)
    timestamp = int(time.time())
    payload = struct.pack('q', timestamp) + str(data).encode()

    # create checksum
    check = checksum(header + payload)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(check), pack_id, 1)
    payload = struct.pack('q', timestamp) + str(data).encode()
    packet = header + payload

    # send and receive icmp packet
    sock.sendto(packet, (DEST, 0))

    msg1, addr1 = sock.recvfrom(2048)
    msg2, addr2 = sock.recvfrom(2048)
    sock.close()
    message = msg1 if len(msg1) > len(msg2) else msg2
    # print(message[0:32].decode())
    instructions = message[28:].decode()
    # data = message[:7].decode()
    f = open("inst_step5.txt", "w")
    f.write(instructions)
    f.close()
    return instructions[:6]


# The function do checksum of a data
def checksum(data):

    def sum16(data):
        "sum all the the 16-bit words in data"
        if len(data) % 2:
            data += '\0'.encode()

        return sum(struct.unpack("!%sH" % (len(data) // 2), data))

    retval = sum16(data)                       # sum
    retval = sum16(struct.pack('!L', retval))  # one's complement sum
    retval = (retval & 0xFFFF) ^ 0xFFFF        # one's complement
    return retval
