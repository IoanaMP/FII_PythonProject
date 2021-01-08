import os, random, struct
from Crypto import Random
from Crypto.Cipher import AES
import string
import ntpath

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

key = ''.join(random.choices(string.digits, k=16))
fsz = os.path.getsize('C1.mp4')
enc = encrypt_file(key, 'C1.mp4', fsz, out_filename=None)
print(os.path.getsize(enc))
# print(enc)
decrypt_file(key,enc, fsz, out_filename=None)
