# send a file larger than the receive socket buffer size

import socket
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))
print("Connected. Sending file now ...")
with open('2MB.base64', 'rb') as f:
    try:
        print("Bytes sent:", s.sendfile(f, 0))
    except Exception as e:
        print ("Sending threw an error:", e)

print(f"Closing socket.")
s.close()
