import sys
import os
from pathlib import Path

from InputProgram import InputProgram
from checker import check_validity

from utils.Graph import CFG

def main():
    if len(sys.argv) != 3:
        print('Usage: main path/to/input/file.py path/to/output/file.py', file=sys.stderr)
        sys.exit(1)

    if not check_validity(Path(sys.argv[1])):
        print('Input code not valid', file=sys.stderr)
        sys.exit(1)

    block_stack = []
    with open(Path(sys.argv[1]), 'r') as input_file:
        input_program = InputProgram(input_file.read())
        input_program.basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)

        block_id = 1
        block_stack = input_program.get_block_stack()
        for block in input_program.basic_blocks:
            print(block.stringify_block())
            block_id += 1

    cfg = CFG(block_stack)

    from pprint import pprint
    pprint(cfg.graph)

    spanning_tree = cfg.spanning_tree()
    pprint(spanning_tree)


if __name__ == '__main__':
    main()
