import sys,os
from fsplit.filesplit import Filesplit
from pathlib import Path

command = sys.argv[1]
n = int(sys.argv[2])
m = sys.argv[3]
file = sys.argv[4]
print(Path(file).stat().st_size)
split_size = os.stat(file).st_size
fp = Filesplit()

def split_cb(f, s):
    print("file: {0}, size: {1}".format(f, s))


print(len(sys.argv))
if len(sys.argv) != 5:
    print("Not enough data")



chunk = int(split_size/n)
fp.split(file=file, split_size=chunk, callback= split_cb, newline = True)
split_size -= chunk


print(command)
print(n)
print(file)


