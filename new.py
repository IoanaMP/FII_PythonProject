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
    coeffici = []
    for _ in range(m - 1):
        coeffici = [random.randrange(0, secret_size)]
    coeffici.append(secret_size)
    # print("coef", coeffici)
    return coeffici

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

    count = 0
    dest_dir = Path().absolute()
    for i in range(n):
        splited_data = []
        rand = random.randrange(1,max)
        data = polynom(rand, coef)
        splited_data.append(rand)
        splited_data.append(data)
        count += 1
        filename = os.path.join(dest_dir, ('File%02d' % count + '.txt'))
        if filename in os.listdir(dest_dir):
            os.remove(os.path.join(dest_dir, filename))
        final_file = open(filename, 'w')
        final_file.write(str(splited_data))

def recompose(files):
    """
    Aplic interpolarea Lagrange pe datele pentru a obtine din nou fisierul initial
    """
    sum = 0
    s = len(files)
    for i in range(s):
        x1, y1 = int(files[i][0]), int(files[i][1])
        produs = 1
        for j in range(s):
            x2 = int(files[j][0])
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
    print('sz', size)
    split(file, size, n, m)

    print("Enter the recompose command(file.py -recompose file.ext file.ext etc)")
    dest_dir = Path().absolute()
    command = input().split()
    if command[1] != "-recompose":
        print("Incorrect command")
        exit()
    i = 2
    files = []
    while i < len(command):
        fis = open(command[i], 'r')
        dt = fis.read()
        l = len(dt) - 1
        dt = dt[1:l]
        nr = dt.split(', ')
        files.append(nr)
        i += 1
    print(files)
    rsize = recompose(files)
    print('rsz', rsize)
    filename = os.path.join(dest_dir, (fname+'_r'+ext))
    final_file = open(filename, 'wb')
    final_file.write(rsize)
