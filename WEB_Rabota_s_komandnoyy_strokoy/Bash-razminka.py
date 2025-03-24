import sys

try:
    if len(sys.argv) != 3:
        print(0)
    else:
        print(int(sys.argv[1]) + int(sys.argv[2]))
except ValueError:
    print(0)