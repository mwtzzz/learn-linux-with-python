# basic server
# single threaded, handle one connection at a time until it closes
# then move to the next

import socket
import time
import datetime
from queue import Queue

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
bytes_to_drain = 16

# loop forever
while True:
    # the following blocks until a new connection
    print("Waiting for a new connection.")
    conn, addr = sock.accept()
    print(f"Accepted a connection from {addr}. Waiting to receive data ...")
    # the following blocks until new data
    data = conn.recv(bytes_to_drain) # how much data to receive on this read
    while data:
        print("Received data.")
        request = str(data, "utf-8")
        print(f"Received request:\n{request}. Sending reply.")
        conn.sendall(bytes("Reply\n", "utf-8"))
        data = conn.recv(bytes_to_drain)
    print("No more data.")
    if not data:
        print("Empty request, skipping.")
        continue
    time.sleep(15)
