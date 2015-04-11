#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from Server import initDict




def initTable():
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor()    
        cur.execute("DROP TABLE Rainbow;")
        cur.execute("CREATE TABLE Rainbow(name TEXT, tth TEXT,time LONG)")
    #    cur.execute("INSERT INTO Rainbow(name) VALUES ('azaz');")

    


def remplissage(uneListe) :
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        for i in uneListe:
            cur.execute("INSERT INTO Rainbow(name) VALUES (?);",(i,))
            
def recherche(tth):
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        cur.execute("SELECT tth FROM Rainbow WHERE tth = ?;",(tth,))
        return cur.fetchall()

def rechercheTravail():
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        cur.execute("SELECT name FROM Rainbow WHERE tth IS NULL;")
        return cur.fetchone()[0]
        
def returnTravail(name, tth):
    con = lite.connect('rainbowtable.db')
    with con:
        cur = con.cursor() 
        cur.execute("UPDATE Rainbow SET tth=? WHERE name=?;",(tth,name))
        
    
    
        



    
def readTable():
    con = lite.connect('rainbowtable.db')
    with con:    
        cur = con.cursor()    
        cur.execute("SELECT * FROM Rainbow")
        rows = cur.fetchall()
        for row in rows:
            print row
