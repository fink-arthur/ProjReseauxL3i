#!/usr/local/bin/python3    # This is server.py file

import socket               # Import socket module
import random
from thread import start_new_thread
from TTH import TTH
import sys, getopt
from baseDeDonnee import *

def initDict(chemin) :
  with open(chemin) as ins:
    array = []
    for line in ins:
        array.append(line.rstrip())    
  return array

def boucleinterne(mot):
  liste = []
  for j in range(1,27):
      motinter = mot
      liste.append(mot + chr(96 + j))
  return liste

def inputthread():
  while True:
    string = raw_input("Entrer une chaine de caracteres: ")
    res = TTH((0,0,0,0),string)
    print(res)

def clientthread(c):
  while True:
     msg = c.recv(1024).decode('UTF-8')
     if(msg == "GET\n"):
         c.sendall("SET " + rechercheTravail() + "\n")
         msg = c.recv(1024).decode('UTF-8')
         if (msg[:6] == "RETURN"):
            acc = msg.rstrip().split(" ")
            returnTravail(acc[1], acc[2])
            print(msg)

if __name__ == "__main__":

  port = 2048                # Reserve a port for your service.

  try:
      opts, args = getopt.getopt(sys.argv[1:],"hp:c:f:",["parg=","carg=","farg="])
  except getopt.GetoptError:
      print 'Server.py -p <numeroPort> -c <nbrMaxConnection> -f <fichierDictionnaire>'
      sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Server.py -p <numeroPort> -c <nbrMaxConnection> -f <fichierDictionnaire>'
      sys.exit()
    elif opt in ("-p", "--parg"):
      port = arg
    elif opt in ("-c", "--carg"):
      pass
    elif opt in ("-f", "--farg"):
      pass

  # Mise en place du serveur
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
  host = socket.gethostname() # Get local machine name
  s.bind((host, port))        # Bind to the port
  

  initTable()
  liste = initDict('dict.txt')
  # Ecoute sur le socket
 
  remplissage(liste)
  
  #readTable()
  
  start_new_thread(inputthread,())
  s.listen(5)                 # Now wait for client connection.
  while (True):
    c, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    start_new_thread(clientthread, (c,)) # dedicasse a Julien
