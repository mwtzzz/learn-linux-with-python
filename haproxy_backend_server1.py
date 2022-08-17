#!/usr/bin/env python3

""" Simple TCP Server
* respond to simple commands
* can be used to illustrate persistent connections through HAProxy
* each thread handles a connection simultaneous and independent
* do not use Queue because is FIFO which can't be parallelized
"""

import socket
import threading
from threading import Thread
import re

servername = "A"
port = 9999
max_open_connections = 50
active_connections = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", port))
sock.listen()

def process_connection(conn, addr):
    """Handles an incoming tcp connection.
    Close if too much data is read.
    Close if the other end closes.

    """

    global active_connections
    threadId = threading.get_ident()
    print(f"Server {servername}, Thread {threadId}: Procesing connection {addr}")
    while True: # persistent connection, keep processing
        try:
            # blocks until new data in socket buffer
            data = conn.recv(8)
            if len(data) > 6:
                print(f"Server {servername}, Thread {threadId}: Received too much. Closing this connection.")
                break
            command = str(data, encoding="utf-8")
            print(f"Server {servername}, Thread {threadId}: Received command: {command}.")
            if re.search("status", command):
                conn.sendall(bytes(f"Server {servername}, thread {threadId}: Health ok.", "utf-8"))
            else:
                conn.sendall(bytes(f"Server {servername}, thread {threadId}: Invalid command, try again.", "utf-8"
))
        except Exception as e:
            print(f"Server {servername}, Thread {threadId}: Error {e}. Closing thread.")
            break

    conn.close()
    active_connections -= 1

while True:
    print(f"Server {servername} Waiting for a new connection ...")
    conn, addr = sock.accept() # blocks until there is a connection
    active_connections += 1
    if active_connections > max_open_connections:
        print(f"Server {servername}: Number of allowed connections exceeded, closing new connection.")
        conn.close()
        active_connections -= 1
    else:
        t = Thread(target=process_connection, args=(conn, addr))
        t.start()
