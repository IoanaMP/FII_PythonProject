import os
import sys
from pathlib import Path
import ntpath


def split(source, size, n):
    dest_dir = Path().absolute()
    input_file = open(source, 'rb')
    count = 0
    f = ntpath.split(source)[1]
    fname, ext = os.path.splitext(f)
    for i in range(0,n-1):
        chunk = int(size / n)
        size = size - chunk
        chunk_f = input_file.read(chunk)
        if not chunk_f:
            break
        count += 1
        filename = os.path.join(dest_dir, ( fname+'%04d' % count + ext))
        if filename in os.listdir(dest_dir):
            os.remove(os.path.join(dest_dir, filename))
        final_file = open(filename, 'wb')
        final_file.write(chunk_f)
        final_file.close()
    chunk = size
    chunk_f = input_file.read(chunk)
    count += 1
    filename = os.path.join(dest_dir, (fname +'%04d' % count + ext))
    if filename in os.listdir(dest_dir):
        os.remove(os.path.join(dest_dir, file))
    final_file = open(filename, 'wb')
    final_file.write(chunk_f)
    final_file.close()
    input_file.close()


if __name__ == '__main__':
    print("Enter a command")
    com = input().split()

    if len(com) < 4:
        print("Not enough data")
    if com[1] == "-split":
        n = int(com[2])
        m = int(com[3])
        file = com[4]
        file_size = os.stat(file).st_size
        split(file, file_size, n)
    elif com[1] == "-recompose":
        dest = Path().absolute()
        f = ntpath.split(com[2])[1]
        fname, ext = os.path.splitext(f)
        out = "File_recomposed" + ext
        if out in os.listdir(dest):
            os.remove(os.path.join(dest, out))
        output = open(out, 'wb')
        i = 2
        while i<len(com):
            f = com[i]
            size = os.stat(f).st_size
            rd = open(f, 'rb')
            while True:
                bytes = rd.read(size)
                if not bytes:
                    break
                output.write(bytes)
            i += 1
            rd.close()
        output.close()
    else:
        print("Command unknown")
