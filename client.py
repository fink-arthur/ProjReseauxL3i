#!/usr/local/bin/python3    # This is client.py file

import socket               # Import socket module
import time
from TTH import TTH

while (True):
    # Connection au serveur
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 2048                # Reserve a port for your service.
    s.connect((host, port))


    # Le client envoie GET au serveur
    s.sendall("GET\n")

    # Le client recoit son SET et la chaine a hasher et ferme la connexion
    msg = s.recv(1024).decode('UTF-8')
    
    if (msg == "NOPE plus de travail"):
    	exit(0)
    else:
	    # Le client effectue le travail
	    msg = msg.split(" ")[1]
	    res = TTH((0,0,0,0),msg)

	    ## le client envoie le RETURN
	    s.sendall("RETURN " + msg + " " + res + "\n")
	    s.close                     # Close the socket when done
	    time.sleep(5)

# from http://www.tutorialspoint.com/python/python_networking.htm
# autre ref: http://docs.python.org/3.1/howto/sockets.html
