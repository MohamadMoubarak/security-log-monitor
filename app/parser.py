def read_lines(path):
    with open(path) as f:
        for line in f:
            print(line.strip())

read_lines("samples/auth.log")