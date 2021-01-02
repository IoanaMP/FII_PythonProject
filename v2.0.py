import sys,os
from fsplit.filesplit import Filesplit
from pathlib import Path

fp = Filesplit()
def split_cb(n, f, s):
    for i in range(0,n):
        print("file: {0}, size: {1}".format(f, s))


print(len(sys.argv))
if len(sys.argv) != 5:
    print("Not enough data")

command = sys.argv[1]
n = int(sys.argv[2])
m = sys.argv[3]
file = sys.argv[4]
print(Path(file).stat().st_size)
split_size = os.stat(file).st_size

chunk = int(split_size/n)
fp.split(n, file=file, split_size=chunk, callback= split_cb, newline = True)
split_size -= chunk


# print(command)
# print(n)
# print(file)
# with open(file) as file_to_Split:
