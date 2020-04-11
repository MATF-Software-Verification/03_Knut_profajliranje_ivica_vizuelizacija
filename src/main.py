import sys
from src.InputProgram import InputProgram

def main():
    if len(sys.argv) != 2:
        print("Usage: main path/to/file")
        exit()

    with open(sys.argv[1], 'r') as input:
        input_program = InputProgram(input.read())
        basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)
        for block in basic_blocks:
            print(block)

if __name__ == '__main__':
    main()