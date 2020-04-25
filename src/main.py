import sys
from src.InputProgram import InputProgram
from src.checker import check_validity


def main():
    if len(sys.argv) != 2:
        print('Usage: main path/to/file')
        exit()

    if not check_validity(sys.argv[1]):
        print('Input code not valid')
        exit()

    with open(sys.argv[1], 'r') as input_file:
        input_program = InputProgram(input_file.read())

        basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)
        for block in basic_blocks:
            print(block)


if __name__ == '__main__':
    main()
