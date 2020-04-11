from src.BasicBlock import BasicBlock

class InputProgram:
    def __init__(self, code):
        self.instructions = self.make_instructions(code)
        self.basic_blocks = self.divide_into_basic_blocks

    def make_instructions(self, code):
        return code.split('\n')

    def divide_into_basic_blocks(self, instructions):
        leaders = self.get_leaders(instructions)
        basic_blocks = []

        for instruction in instructions:
            if leaders.__contains__(instruction):
                basic_blocks.append(BasicBlock(instruction))
            basic_blocks[-1].add_instruction(instruction)

        return basic_blocks

    def get_leaders(self, instructions):
        leaders = [instructions[0]]
        control_flow_changers = ['if', 'else', 'elif']

        for i in range(len(instructions)):
             if any(cfc in instructions[i] for cfc in control_flow_changers):
                if i + 1 != len(instructions):
                    leaders.append(instructions[i+1])

        return list(set(leaders))

