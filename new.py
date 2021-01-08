"""
 Shamir's Secret Sharing:
 -split: n - in cate parti impartim fisierul, m - de cate parti avem nevoie sa reconstruim fisierul
    To do: Construim un polinom aleatoriu P  cu gradul m-1, setam coeficientul termenului liber egal cu dimensiunea fisierului
        cele n bucati trebuie sa fie n puncte situate pe polinom
        si partile distribuite sunt de fapt coordonatele alese...
 -recompose:
    To do: avem nevoie de cel putin m parti, folosim polinomul de interpolare Lagrange sa contruim polinomul
    din cele m parti date(pentru a avea din nou dimensiunea initiala in P(0)..)
"""

import os
import sys
from pathlib import Path
import ntpath

def extended_Euclid():
    pass

def polynom(X,c):

    sum = []
    coef = len(c)
    for i in range(coef):
        sum += X**(coef-i-1) * c[i]
    return sum

def coefficient(m, secret_size):
    pass

def split(file, size, n, m):
    pass

def recompose():
    pass

if __name__ == '__main__':
    print("Enter a file to be splitted")
    command = input().split()
    file = command[4]
    size = os.stat(file).st_size
    f = open (file, 'rb')
    n = int(command[2])
    m = int(command[3])
    split(file, size, n, m)