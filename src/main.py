import sys
import os
from pathlib import Path

from src.InputProgram import InputProgram
from src.checker import check_validity

def main():
    if len(sys.argv) != 3:
        print('Usage: main path/to/input/file.py path/to/output/file.py', file=sys.stderr)
        sys.exit(1)

    if not check_validity(Path(sys.argv[1])):
        print('Input code not valid', file=sys.stderr)
        sys.exit(1)

    with open(Path(sys.argv[1]), 'r') as input_file:
        input_program = InputProgram(input_file.read())

        block_id = 1
        basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)
        for block in basic_blocks:
            print(block.stringify_block())
            block_id += 1


if __name__ == '__main__':
    main()
