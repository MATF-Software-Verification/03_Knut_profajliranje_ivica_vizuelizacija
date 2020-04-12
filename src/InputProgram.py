from src.BasicBlock import BasicBlock
import re

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
        function_call = re.compile('\w+\([\w\s\d|,]*\)')

        for i in range(len(instructions)):
            function_call_occurs = function_call.findall(instructions[i])
            if any(cfc in instructions[i] for cfc in control_flow_changers) or 0 != len(function_call_occurs):
                if i + 1 != len(instructions):
                    leaders.append(instructions[i+1])

        return list(set(leaders))

