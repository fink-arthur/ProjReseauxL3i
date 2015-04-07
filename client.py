#!/usr/local/bin/python3    # This is client.py file

import socket               # Import socket module
msg=''
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print (s.recv(1024).decode('UTF-8'))
s.close                     # Close the socket when done

# from http://www.tutorialspoint.com/python/python_networking.htm
# autre ref: http://docs.python.org/3.1/howto/sockets.html
