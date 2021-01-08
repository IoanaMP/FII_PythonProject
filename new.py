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
    global max
    max = 1000000
    if m > n:
        raise ValueError("The threshold can not be greater than the number of shares")
    coef = coefficient(m, size)
    splited_data = []
    count = 0
    for i in range(n):
        rand = random.randrange(1,max)
        data = polynom(rand, coef)
        splited_data.append([rand, data])
        count += 1
        filename = os.path.join(dest_dir, ('File%02d' % count + '.txt'))
        final_file = open(filename, 'w')
        final_file.write(str(splited_data))

def recompose(files):
    """
    Aplic interpolarea Lagrange pe datele pentru a obtine din nou fisierul initial
    """
    sum = 0
    s = len(files)
    for i in range(s):
        x1, y1 = files[i][0], files[i][1]
        produs = 1
        for j in range(s):
            x2 = files[j][0]
            if i!=j:
                produs *= x2/(x2-x1)
        produs *= y1
        sum += produs
    return int(round(sum,0))


if __name__ == '__main__':

    print("Enter the split command(file.py -split no_shares threshold File_tobe_split.ext)")
    command = input().split()
    if command[1] != "-split" or len(command) != 5:
        print("Incorrect command")
        exit()
    n = int(command[2])
    m = int(command[3])
    file = command[4]
    f = ntpath.split(file)[1]
    fname, ext = os.path.splitext(f)
    size = os.stat(file).st_size
    split(file, size, n, m)
    global dest_dir
    dest_dir = Path().absolute()
    print("Enter the recompose command(file.py -recompose file.ext file.ext etc)")
    command = input().split()
    if command[1] != "-recompose":
        print("Incorrect command")
        exit()
    i = 2
    files = []
    while i < len(command):
        files.append(command[i])
        i += 1
    rsize = recompose(files)
    filename = os.path.join(dest_dir, (fname+'_r'+ext))
    final_file = open(filename, 'w')
    final_file.write(str(rsize))
