#!/usr/local/bin/python3    # This is server.py file
# -*- coding: utf-8 -*-

import socket
import random
from thread import start_new_thread
import thread
from TTH import TTH
import sys, getopt
from baseDeDonnee import *
import re

def initDict(chemin):
   """
   Lis tous les lignes d'un fichier a l'adresse chemin et les mets dans un array
   """
   with open(chemin) as ins:
      array = []
      for line in ins:
         array.append(line.rstrip())    
   return array
       
def DIC():
   """
   Cree tous les mots de 4 lettres et les met dans un array
   """
   liste = []
   for i in range(26):
	for j in range(26):
		for k in range(26):
			for l in range(26):
				liste.append(chr(i+97)+chr(j+97)+chr(k+97)+chr(l+97))
   return liste
                      
def inputthread():
   """
   Thread qui attends un input (qui va passer dans TTH) de l'utilisateur pour en chercher les collisions
   """
   while True:
      string = raw_input("Entrer une chaine de caracteres: ")
      res = TTH((0,0,0,0),string)
      rechercheCollision(res)
     
def rechercheCollision(mot):
   """
   Prend un tth et renvoie tous les mots de la BDD avec le meme tth
   """
   listeCollision = recherche(mot)
   print("COLLISION de "+mot+" :"+parseCollision(listeCollision))
   
def parseCollision(L):  ## COLLISION de epir :[(u'abord',), (u'aborda',)]
    """
    Methode qui affiche bien la collision
    """
    res = ""
    if (len(L) == 0):
        return "le travail n'a pas été encore éffectué pour ce mot"
    else :
        for i in range (len(L)) :
            res = L[i][0] + " " +res
        return res
          
def clientthread(c):
   """
   Thread qui va gerer la connection avec un client
   """
   global iterateur
   carryover = ""
   travail = ""
   ret = re.compile("RETURN [a-z.-]+ [a-z]+\\n") # On verifie que le message est bien de la bonne forme
   c.settimeout(10)


   ########################################
   #                                      #
   #      Mise en place du client         #
   #                                      #
   ########################################

   while True:

      # On regarde si l'envoie du get par le client n'as pas ete trop rapide
      if (carryover == ""):
         try:
            msg = c.recv(1024).decode('UTF-8')
            # Si timeout on ferme la connexion
         except:
            continue
      else:
         msg = carryover + "\n"
         carryover = ""

      # On regarde si le premier message est bien GET
      if(msg == "GET\n"):

         # On regarde si l'iterateur qui nous donne le travail est vide
         try:
            travail = iterateur.next()
         except:
            recherche = rechercheTravail()
            if (len(recherche) == 0): # Plus de travail a faire dans la BDD
               iterateur = None
            else:
               iterateur = recherche.__iter__()
         
         if (iterateur == None): # On endort le client car plus de travail
            c.sendall("NOPE 1\n")
         else:

            # On donne le travail
            if (travail == ""):
               travail = iterateur.next()
            c.sendall("SET " + travail[0] + "\n")
            travail = ""

            # On recoit normalement le RETURN du client
            try:
               msg = c.recv(1024).decode('UTF-8')
            # Si timeout on ferme la connexion
            except:
               c.close()
               thread.exit()
            if (ret.match(msg) != None):
               acc = msg.rstrip().split(" ")
               returnTravail(acc[1], acc[2])
               if (len(msg.split("\n")) == 3):
                  carryover = msg.split("\n")[1]
               #print(msg)

            # Le message n'est pas RETURN
            else :
               c.sendall("NOPE 2\n")
               print(msg)
               c.close()
               thread.exit()

      # Le premier message n'est pas GET mais autre chose
      else :
         c.sendall("NOPE 2\n")
         print(msg)
         c.close()

if __name__ == "__main__":

   port = 2048                # Reserve a port for your service.
   nbClient = 5                  # number of max clients
   liste = None

   ########################################
   #                                      #
   #        On gere les options           #
   #                                      #
   ########################################

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
         nbClient = int(arg)
      elif opt in ("-f", "--farg"):
         liste = initDict(arg)


   ########################################
   #                                      #
   #        On initialise la BDD          #
   #                                      #
   ########################################
  

   t = initTable()

   # Ecoute sur le socket
 
   if (t == 0):
      if (liste == None):
         remplissage(DIC())
      else:
         remplissage(liste)
   
   
   recherche = rechercheTravail()
   if (len(recherche) == 0):
      iterateur = None
   else:
      iterateur = recherche.__iter__()


   ########################################
   #                                      #
   #      Mise en place du serveur        #
   #                                      #
   ########################################


   s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)   # Create a socket object
   host = '127.0.0.1'                                       # Get local machine name
   s.bind((host, port))                                     # Bind to the port
  
   start_new_thread(inputthread,())
   s.listen(nbClient)                  # Now wait for client connection.
   while (True):
      try:
         c, addr = s.accept()          # Establish connection with client.
         print ('Got connection from', addr)
         start_new_thread(clientthread, (c,)) # Dedicasse a Julien	
      except KeyboardInterrupt:
         s.close()
         sys.exit()