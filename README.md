# FII_PythonProject
Python Project: Secret share, Category B, ID 33

Realizați un utilitar care să împartă un fișier în n fișiere. Pentru a recompune fișierul, va fi
necesară prezența a cel puțin m dintre ele.

Input example:
secretshare.py -split 3 2 secret.txt
secretshare.py -recompose file1.secret file2.secret OR
secretshare.py -recompose file2.secret file3.secret OR
secretshare.py -recompose file1.secret file3.secret
file1 -> part1 și part2
file2 -> part2 și part3
file3 -> part1 și part3
