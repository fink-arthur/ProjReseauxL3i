#!/usr/local/bin/python3    # This is client.py file

import socket               # Import socket module
import time
from TTH import TTH


port = 2048                # Reserve a port for your service.
nbClient=5                  # number of max clients
host = socket.gethostname() # Get local machine name
  try:
      opts, args = getopt.getopt(sys.argv[1:],"hp:",["parg=","harg"])
  except getopt.GetoptError:
      print 'Server.py -p <numeroPort> -h <host>'
      sys.exit(2)
  	     

  for opt, arg in opts:
    if opt == '-h':
      print 'Server.py -p <numeroPort> -h: <host>'
      sys.exit()
    elif opt in ("-p", "--parg"):
      port = int(arg)
    elif opt in ("-h", "--carg"):
        host=arg
    

port = 2048       
# Connection au serveur
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
s.connect((host, port))

while(True):
    # Le client envoie GET au serveur
    s.sendall("GET\n")

    # Le client recoit son SET et la chaine a hasher et ferme la connexion
    msg = s.recv(1024).decode('UTF-8')
    
    if (msg == "NOPE 1\n"):
    	time.sleep(60)
    elif (msg == "NOPE 2\n"):
        s.close()
        exit(0)
    elif (msg[:3] == "SET"):
	    # Le client effectue le travail
        msg = msg.rstrip().split(" ")[1]
        res = TTH((0,0,0,0),msg)
	    ## le client envoie le RETURN
        s.sendall("RETURN " + msg + " " + res + "\n")
        #time.sleep(0.0005)
    else:
        print("Il y a une couille")
