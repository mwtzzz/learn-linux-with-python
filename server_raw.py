# display frames from the loopback interface

import socket
import time
import datetime
import sys
import binascii

ETH_P_ALL=3 # not defined in socket module, sadly...
# SOCK_RAW to include the link-level header
# htons(ETH_P_ALL): receive all protocols
s=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

BYTES_TO_RECV=2048
TIME_TO_SLEEP=0
s.bind(("lo", 0)) # loopback makes it easy to see your test packets
r=s.recv(BYTES_TO_RECV) # pop 2048 bytes off the socket buffer
while r:
    hexvalue=binascii.hexlify(r) # convert the buffer data into hex
    print([hexvalue[i:i+2] for i in range(0, len(hexvalue), 2)])
    time.sleep(TIME_TO_SLEEP) # this proves that frames are queued in the receive buffer
    r=s.recv(BYTES_TO_RECV) # pop the next 2048 bytes off the socket buffer
