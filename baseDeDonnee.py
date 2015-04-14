#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

def initTable():
    """
    Fonction qui initialise la table de la BDD
    """
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor()    
        cur.execute("DROP TABLE Rainbow;")
        cur.execute("CREATE TABLE Rainbow(name TEXT, tth TEXT,time LONG)")

def remplissage(uneListe):
    """
    Fonction qui remplit la table en initialisant seulement le champ name, 
    pour chaque element de la liste
    """
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        for i in uneListe:
            cur.execute("INSERT INTO Rainbow(name) VALUES (?);",(i,))
            
def recherche(tth):
    """
    Fontion qui recherche dans la BDD tous les mots qui ont le meme tth que celui donné en argument
    """
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        cur.execute("SELECT name FROM Rainbow WHERE tth = ?;",(tth,))  
        return cur.fetchall()

def rechercheTravail():
    """
    Fonction qui recherche le premier mot qui n'as pas encore été traité
    """
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        cur.execute("SELECT name FROM Rainbow WHERE tth IS NULL;")
        return cur.fetchall()

def nextTravail(iterable):
    return iterable.next()
        
def returnTravail(name, tth):
    """
    Fonction qui met a jour la BDD avec la valeur du TTH du mot
    """
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Rainbow SET tth=? WHERE name=?;",(tth,name))
        con.commit()
           
def readTable():
    """
    Fonction qui affiche la table de la BDD
    """
    con = lite.connect('rainbowtable.db')
    with con:    
        cur = con.cursor()    
        cur.execute("SELECT * FROM Rainbow")
        rows = cur.fetchall()
        for row in rows:
            print row