size = 1024
file = 1
with open('Curs-11.pdf') as f:
    split = f.read(size)
    while split:
        with open('file_part_' +str(file)) as splited_file:
            splited_file.write(split)
        file += 1
        split = f.read(size)