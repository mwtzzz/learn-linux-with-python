# same as client4 but without sleeps

import socket
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))
print("Connected. Sending data now ...")
sendstream =  sys.argv[1] + "\n"
for x in range(1,5):
    try:
        print("Bytes sent:", s.send(bytes(sendstream, "utf-8")), sendstream)
    except Exception as e:
        print ("Sending threw an error:", e)
    # to do: may need a timeout around the recv
    print (f"Received: {str(s.recv(16), 'utf-8')}")

print(f"Closing socket.")
s.close()
