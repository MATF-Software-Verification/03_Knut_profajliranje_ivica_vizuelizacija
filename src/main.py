import sys
from src.InputProgram import InputProgram

def main():
    if (len(sys.argv) != 2):
        print("Usage: main.py path/to/input/file")
        exit()

    with open(sys.argv[1], 'r') as input:
        code = input.read()

    print(code)
    input_program = InputProgram(code)
    basic_blocks = input_program.basic_blocks
    for block in basic_blocks:
        print(block.__str__())

if __name__ == '__main__':
    main()