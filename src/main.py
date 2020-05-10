import sys
import os
from pathlib import Path

from src.InputProgram import InputProgram
from src.checker import check_validity
from src.instrumentalization.Instrumentalizator import Instrumentalizator

from utils.Graph import Graph

def main():
    if len(sys.argv) != 3:
        print('Usage: main path/to/input/file.txt path/to/output/file.py', file=sys.stderr)
        sys.exit(1)

    if not check_validity(Path(sys.argv[1])):
        print('Input code not valid', file=sys.stderr)
        sys.exit(1)

    with open(Path(sys.argv[1]), 'r') as input_file:
        input_program = InputProgram(input_file.read())

        basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)
        for block in basic_blocks:
            print(block)

    instrumentalization_out = Path('./instrumentalization_output.txt')
    # instrumentalize source file
    instr = Instrumentalizator(
        Path(sys.argv[1]), Path(sys.argv[2]),
        instrumentalization_out
    )
    instr.instrumentalize()

    print('Running instrumentalized code...', file=sys.stderr)
    print('------------------------------', file=sys.stderr)
    # run newly created and instrumentalized, source file
    command = f'python {Path(sys.argv[2])}'
    os.system(command)

    control_flow_graph = Graph()
    with open(instrumentalization_out, 'r') as instr_out_file:
        control_flow_graph.create_graph_from_blocks(instr_out_file.read())

    spanning_tree = control_flow_graph.create_spanning_tree()

    print('control flow graph:')
    print(control_flow_graph.edges())
    print(control_flow_graph.nodes())

    print('spanning tree:')
    print(spanning_tree.edges())
    print(spanning_tree.nodes())


if __name__ == '__main__':
    main()
