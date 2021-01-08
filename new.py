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
import random
import ntpath

def extended_Euclid():
    pass


def polynom(X,c):
    """
    c- e lista coeficientul(dimensiunea fisierului) si puterea lui X(al n-lea fisier)
    X**(coef-i-1): X la putera m-1, m-2,..,0
    sum va fi rezultatul polynomului
    """
    coef = len(c)
    return sum([X**(coef-i-1) * c[i] for i in range(coef)])


def coefficient(m, secret_size):
    pass

def split(file, size, n, m):
    """
    fac polinomul cu valori random pentru coeficienti
    pun valoarea "secretului" in file.secret(le-am pus in fisiere txt) sa le pot da ca argumente pentru recompose
    """
    global max;
    max = 1000000
    if m > n:
        raise ValueError("The threshold can not be greater than the number of shares")
    coef = coefficient(m, size)
    splited_data = []
    dest_dir = Path().absolute()
    f = ntpath.split(file)[1]
    fname, ext = os.path.splitext(f)
    count = 0
    for i in range(n):
        rand = random.randrange(1,max)
        data = polynom(rand, coef)
        splited_data.append([rand, data])
        count += 1
        filename = os.path.join(dest_dir, (fname + '%02d' % count + '.txt'))
        final_file = open(filename, 'w')
        final_file.write(str(splited_data))

def recompose():
    pass


if __name__ == '__main__':

    print("Enter the split command(file.py -split no_shares threshold File_tobe_split.ext)")
    command = input().split()
    action = command[1]
    if action != "-split" or len(command) != 5:
        print("Incorrect command")
        exit()
    n = int(command[2])
    m = int(command[3])
    file = command[4]
    size = os.stat(file).st_size
    split(file, size, n, m)
    print("Enter the recompose command(file.py -recompose file.ext file.ext etc)")
    command = input().split()
