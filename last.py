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
        filename = os.path.join(dest_dir, ('File%04d' % count + ext))
        fileobj = open(filename, 'wb')
        fileobj.write(chunk_f)
        fileobj.close()
    chunk = size
    chunk_f = input_file.read(chunk)
    count += 1
    filename = os.path.join(dest_dir, ('File%04d' % count + ext))
    fileobj = open(filename, 'wb')
    fileobj.write(chunk_f)
    fileobj.close()
    input_file.close()


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Not enough data")
    command = sys.argv[1]

    if command == "-split":
        n = int(sys.argv[2])
        m = sys.argv[3]
        file = sys.argv[4]
        file_size = os.stat(file).st_size
        split(file, file_size, n)
    elif command == "-recompose":
            file_re = open(sys.argv[2], "wb")
            i = 3
            while sys.argv[i]:
                rd = open(sys.argv[i], "rb")
                size = os.stat(rd).st_size
                while True:
                    bytes = rd.read(size)
                    if not bytes:
                        break
                    file_re.write(bytes)
                i += 1
                rd.close()
            file_re.close()
            print(file_re)
    else:
        print("Command unknown")
