"""
 Cum algoritmul lui Shamir functioneaza pe numere si nu prea ai un mod de a reconstrui fisierul:
 << ai dreptate, nu sunt părți as in părți disjuncte...
  dacă fișierul inițial are 10kb și vrei să îl împarți în 5, nu o să aibă fiecare câte 2kb...
  more likely e să aibă fiecare tot 10kb,de asta e foarte ambiguu și îmi cer scuze
  uite, îți dau altă idee care e validă pentru proiectul ăsta, cred că mai degrabă așa se folosește out there
 poți cripta tot fișierul folosind un algoritm de criptare (poți folosi unul pe care îl găsești), și să aplici Shamir doar pe cheia de decriptare>>
 Shamir's Secret Sharing:
 -split: n - in cate parti impartim fisierul, m - de cate parti avem nevoie sa reconstruim fisierul
    To do: Construim un polinom aleatoriu P  cu gradul m-1, setam coeficientul termenului liber egal cu dimensiunea fisierului
        cele n bucati trebuie sa fie n puncte situate pe polinom
        si partile distribuite sunt de fapt coordonatele alese...
 -recompose:
    To do: avem nevoie de cel putin m parti, folosim polinomul de interpolare Lagrange sa contruim polinomul
    din cele m parti date(pentru a avea din nou dimensiunea initiala in P(0)..)
    Daca tot s-au permis sursele externe pentru criptare, am folosit urmatorul link(dar tot eu l-am facut sa si mearga)
    https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
"""

import string
import os
import struct
from Crypto import Random
from Crypto.Cipher import AES
from random import randint
from pathlib import Path
from decimal import *
import random
import ntpath
import csv

def encrypt_file(key, in_filename, chunksize, out_filename=None):
    f = ntpath.split(in_filename)[1]
    fname, ext = os.path.splitext(f)
    if not out_filename:
        out_filename = 'Encrypted_file' + ext

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    blocks = (16 - len(chunk) % 16) % 16
                    chunk += chr(0).encode("utf8") * blocks

                outfile.write(encryptor.encrypt(chunk))
    return out_filename

def decrypt_file(key, in_filename, chunksize, out_filename=None):
    f = ntpath.split(in_filename)[1]
    fname, ext = os.path.splitext(f)
    if not out_filename:
        out_filename = 'TheSecret' + ext
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    blocks = (16 - len(chunk) % 16) % 16
                    chunk += chr(0).encode("utf8") * blocks
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)

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

def split(size, n, m):
    """
    fac polinomul cu valori random pentru coeficienti
    pun valoarea "secretului" in file.secret(le-am pus in fisiere txt) sa le pot da ca argumente pentru recompose
    """
    max = 100000
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
    deci fara Decimal nu merge ok pe numere foarte mari cum e cheia de 16biti
    """
    sum = 0
    s = len(files)
    for i in range(s):
        x1, y1 = int(files[i][0]), int(files[i][1])
        produs = Decimal(1)
        for j in range(s):
            x2 = int(files[j][0])
            if i != j:
                produs *= Decimal(Decimal(x2)/(x2-x1))
        produs *= y1
        sum += produs
    return int(round(Decimal(sum),0))


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
    key = ''
    key = key + str(randint(1,9))
    for i in range(15):
        key = key + str(randint(0, 9))
    print(key)
    encripted_secret = encrypt_file(key, file, size, out_filename=None)
    split(int(key), n, m)

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
    comp_key = recompose(files)
    the_key = str(comp_key)
    print('cheie recompusa', comp_key)
    decrypt_file(the_key, encripted_secret, size, out_filename=None)

