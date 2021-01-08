import random, string
import os
import struct
from Crypto import Random
from Crypto.Cipher import AES

# x = ''.join(random.choices(string.digits, k=16))
# print(x)
# key = os.urandom(16)
# print('key', key)
key = ''.join(random.choices(string.digits, k=16))
iv = Random.new().read(AES.block_size)
print(iv)
aes = AES.new(key, AES.MODE_CBC, iv)
data = 'hello world 1234' # <- 16 bytes
encd = aes.encrypt(data)
print(encd)
aes = AES.new(key, AES.MODE_CBC, iv)
decd = aes.decrypt(encd)
print(decd)

file = open('Curs-11.pdf', 'rb')
fsz = os.path.getsize('Curs-11.pdf')
infile = file.read(fsz)

fout = open('encfile.pdf', 'wb')
fout.write(struct.pack('<Q', fsz))
fout.write(iv)
sz = 2048
fin = open('Curs-11.pdf', 'rb')

while True:
    data = fin.read(sz)
    n = len(data)
    if n == 0:
        break
    elif n % 16 != 0:
        data += ' ' * (16 - n % 16)  # <- padded with spaces
    encd = aes.encrypt(data)
    fout.write(encd)
fout.close()
fin.close()

with open('encfile.pdf', 'rb') as fin:
    fsz = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
    iv = fin.read(16)
aes = AES.new(key, AES.MODE_CBC, iv)

with open('file.pdf', 'wb') as fout:
    while True:
        data = fin.read(sz)
        n = len(data)
        if n == 0:
            break
        decd = aes.decrypt(data)
        n = len(decd)
        if fsz > n:
            fout.write(decd)
        else:
            fout.write(decd[:fsz])  # <- remove padding on last block
        fsz -= n