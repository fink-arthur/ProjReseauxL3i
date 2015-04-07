'''
Created on 5  may 2013
@author: Guy Barshap
Modified on march 30 2015
@author: Bruno Martin
'''

import numpy as np

# text="I leave twenty million dollars to my friendly cousin Bill" # TTH() -> b f q g
# text="AYHGD" # TTH() -> b f q g

def TTH(IV,text):
    def shiftlist(l,n): #this function shifts the list
        l=list(l)
        Shifted=l[n:]+l[:n]
        return Shifted

    def toNum(text):
        text=text.replace(" ",'')                   #ignore spaces
        text=text.lower()                           #ignore case sensitive
        # adds padding as sequence of a's in the end
        if len(text)%16 != 0 :
            longueur=16*((len(text)//16)+1)
            text=text+"a"*(longueur-len(text))
        textN=[ord(c)-97 for c in text]              #convert text to ascii
        return textN

    def toChar(L):
        M=list(map(lambda x: chr(x+97) ,L))
        return M

    textAsNumbers=toNum(text)
    lenght = len(textAsNumbers)                      # move 16 char every time..
    for x in range(int(lenght/16)):                  # iterates over the blocks of length 16
        Matrix =np.array(textAsNumbers[16*x:16*(x+1)]).reshape(4,4) #convert 16 string to 4X4 matrix
        sumMatrix=(Matrix.sum(axis=0))               #sum the Matrix
        for x in range(3):                           # rotate each row
            Matrix[x,:] =shiftlist(Matrix[x,:],x+1)
        ########## ugly last row rotation:
        temp =Matrix[3,0];Matrix[3,0]=Matrix[3,3];Matrix[3,3]=temp
        temp =Matrix[3,1];Matrix[3,1]=Matrix[3,2];Matrix[3,2]=temp
        ########## Sum the columns + the rotate colums +IV
        IV=(IV +(Matrix.sum(axis=0))+sumMatrix)%26

    IV2=toChar(IV)
    return ''.join(IV2)


IV=(0,0,0,0) # initial Vector
#print(TTH(IV,input('Entrez la chaine a hacher: ')))


