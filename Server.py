#!/usr/local/bin/python3    # This is server.py file

import socket               # Import socket module
import random
from thread import start_new_thread

# Mise en place du serveur
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 2048                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
compteur = 0

def initDict(chemin) :
  with open(chemin) as ins:
    array = []
    for line in ins:
        array.append(line)
  return array

liste = initListe('dict.txt')

def boucleinterne(mot):
  liste = []
  for j in range(1,27):
      motinter = mot
      liste.append(mot + chr(96 + j))
  return liste

def clientthread(c):
  global compteur
  while True:
     msg = c.recv(1024).decode('UTF-8')
     if(msg == "GET\n"):
         c.sendall("SET " + liste[compteur] + "\n")
         compteur += 1
         print("GET envoyer")
         msg = c.recv(1024).decode('UTF-8')
         if (msg[:6] == "RETURN"):
            print(msg)

# Ecoute sur le socket
s.listen(5)                 # Now wait for client connection.
while (True):
  c, addr = s.accept()     # Establish connection with client.
  print ('Got connection from', addr)
  start_new_thread(clientthread, (c,)) # dedicasse a Julien