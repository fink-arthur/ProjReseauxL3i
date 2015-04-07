#!/usr/local/bin/python3    # This is server.py file

import socket               # Import socket module
import random

# Mise en place du serveur
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 2048                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port


# Ecoute sur le socket
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   msg = c.recv(1024).decode('UTF-8')
   if(msg == "GET\n"):
      if (random.randint(0,5) == 2):
         c.sendall("NOPE " + "plus de travail\n")
      else:
         c.sendall("SET " + "AYHGD\n")
         print("GET envoyer")
         msg = c.recv(1024).decode('UTF-8')
         if (msg[:6] == "RETURN"):
            print(msg)
         
      
   c.close()                # Close the connection
