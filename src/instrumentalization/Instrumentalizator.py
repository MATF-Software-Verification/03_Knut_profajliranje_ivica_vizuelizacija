from pathlib import Path
import sys
import re
import os


class Instrumentalizator():
    def __init__(self, path_to_input, path_to_output, path_to_instrumentalization_output):
        self.input_file = Path(path_to_input)
        self.output_file = Path(path_to_output)
        self.instrumentalization_output_file = Path(path_to_instrumentalization_output)


    def instrumentalization_init(self):
        return f'''
import inspect


instrumentalization_output = open('{self.instrumentalization_output_file}', 'w+')

def print_func_info():
    curr_frame = inspect.currentframe()
    call_frame = inspect.getouterframes(curr_frame, 2)

    print(call_frame[2][3] + ' -> ' + call_frame[1][3], file=instrumentalization_output)
    print('---------------', file=instrumentalization_output)

'''

    def instrumentalize(self):
        input_program = ''
        with open(self.input_file, 'r') as input_file:
            input_program = input_file.read()

        new_source_code = [self.instrumentalization_init()]
        input_program = input_program.split('\n')

        for line in input_program:
            # transfer every line into new source code
            new_source_code.append(line)
            new_source_code.append('\n')

            # if the line is function definition
            # add instrumentalization below it
            find_func_def = re.search(r'^def\s+', line)
            if find_func_def:
                new_source_code.append('    print_func_info()')
                new_source_code.append('\n')

        new_source_code = ''.join(new_source_code)

        with open(self.output_file, 'w') as output_file:
            output_file.write(new_source_code)
            output_file.flush()

        print('------------------------------', file=sys.stderr)
        print('Instrumentalization finished!', file=sys.stderr)
        print('------------------------------', file=sys.stderr)


def main():
    if len(sys.argv) != 3:
        print('Usage: main path/to/input/file.txt path/to/output/file.py', file=sys.stderr)
        sys.exit(1)

    instr = Instrumentalizator(sys.argv[1], sys.argv[2], './instrumentalization_output.txt')
    instr.instrumentalize()

    print('Running instrumentalized code...', file=sys.stderr)
    print('------------------------------', file=sys.stderr)
    # run newly created and instrumentalized, source file
    command = f'python {Path(sys.argv[2])}'
    os.system(command)


if __name__ == "__main__":
    main()
