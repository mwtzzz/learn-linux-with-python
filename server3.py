# receive a large file

import socket
import time
import datetime
from queue import Queue
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
active_connections = Queue()


def bind_service():
    global sock
    global active_connections
    active_connections = Queue()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9999))
    sock.listen(2) # backlog

bind_service()
failures = 0

# the following blocks until a new connection
print("Waiting for a new connection.")
conn, addr = sock.accept()
print("Accepted a connection.")
buffer = bytearray(3000000)
time.sleep(5)

bytes_received = 1
received_file = open("my_received_file", "ab")
while bytes_received > 0:
    bytes_received = conn.recv_into(buffer)
    sys.stdout.write("%d.." % (bytes_received))
    received_file.write(buffer[0:bytes_received])
    time.sleep(1)

conn.close()
received_file.close()
