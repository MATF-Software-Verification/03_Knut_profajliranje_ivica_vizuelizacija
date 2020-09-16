import sys
import os
from pathlib import Path

sys.path.insert(1, '../')
from InputProgram import InputProgram
from checker import check_validity

from utils.Graph import CFG
from utils.Knuth import Knuth

def activate(code):
    block_stack = []
    blocks = []

    input_program = InputProgram(code)
    input_program.basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)

    block_id = 1
    block_stack = input_program.get_block_stack()
    for block in input_program.basic_blocks:
        # print(block.stringify_block())
        blocks.append(block)
        block_id += 1

    from pprint import pprint
    cfg = CFG(block_stack)

    spanning_tree = cfg.spanning_tree()

    spanning_tree_inverse = cfg.spanning_tree_inverse(spanning_tree)

    # instrumentalization TODO


    knuth = Knuth(cfg)

    return blocks
    # pprint(knuth.set_edge_weights())


def main():
    if len(sys.argv) != 3:
        print('Usage: main path/to/input/file.py path/to/output/file.py', file=sys.stderr)
        sys.exit(1)

    if not check_validity(Path(sys.argv[1])):
        print('Input code not valid', file=sys.stderr)
        sys.exit(1)

    input_file = open(Path(sys.argv[1]), 'r')
    output_file = sys.argv[2]
    code = input_file.read()

    blocks = activate(code)

    with open(sys.argv[2], 'w') as output:
        for block in blocks:
            output.write(block.stringify_block())
            output.write('\n')

        output.flush()


if __name__ == '__main__':
    main()
