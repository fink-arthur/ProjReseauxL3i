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
       
def DIC():
    liste = []
    for i in range(26):
	for j in range(26):
		for k in range(26):
			for l in range(26):
				liste.append(chr(i+97)+chr(j+97)+chr(k+97)+chr(l+97))
    return liste
                      
def inputthread():
   while True:
      string = raw_input("Entrer une chaine de caracteres: ")
      res = TTH((0,0,0,0),string)
      rechercheCollision(res)
     
def rechercheCollision(mot):
    listeCollision = recherche(mot)
    print("COLLISION:"+str(listeCollision))

def clientthread(c):
   global iterateur
   carryover = ""
   while True:
      if (carryover == ""):
         msg = c.recv(1024).decode('UTF-8')
      else:
         msg = carryover + "\n"
         carryover = ""
      if(msg == "GET\n"):
         try:
            travail = iterateur.next()
         except StopIteration:
            iterateur = rechercheTravail().__iter__()
            travail = iterateur.next()

         c.sendall("SET " + travail + "\n")
         msg = c.recv(1024).decode('UTF-8')
         if (msg[:6] == "RETURN"):
            acc = msg.rstrip().split(" ")
           # print(port)
            returnTravail(acc[1], acc[2])
            if (len(msg.split("\n")) == 3):
               carryover = msg.split("\n")[1]
          #  print(msg)

if __name__ == "__main__":

   port = 2048                # Reserve a port for your service.
   nbClient=5                  # number of max clients
   liste = initDict('dict.txt')
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
         port = int(arg)
      elif opt in ("-c", "--carg"):
         nbClient=arg
      elif opt in ("-f", "--farg"):
         liste = initDict(arg)

   # Mise en place du serveur
   s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
   host = socket.gethostname() # Get local machine name
   s.bind((host, port))        # Bind to the port
  

   initTable()
  
   # Ecoute sur le socket
 
   remplissage(liste)

   iterateur = liste.__iter__()
  
   #readTable()
  
   start_new_thread(inputthread,())
   s.listen(nbClient)                 # Now wait for client connection.
   while (True):
      try:
         c, addr = s.accept()     # Establish connection with client.
         print ('Got connection from', addr)
         start_new_thread(clientthread, (c,)) # dedicasse a Julien	
      except KeyboardInterrupt:
         s.close()
         sys.exit()