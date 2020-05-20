from src.blocks.BasicBlock import BasicBlock
import re

class InputProgram:
    def __init__(self, code):
        self.instructions = self.make_instructions(code)
        self.basic_blocks = self.divide_into_basic_blocks

    def make_instructions(self, code):
        code = code.split('\n')
        instructions = []
        for instruction in code:
            if instruction.strip() != '':
                instructions.append(instruction)
        return instructions

    def divide_into_basic_blocks(self, instructions):
        leaders = self.get_leaders(instructions)
        basic_blocks = []

        for i in range(len(leaders)-1):
            current_leader = leaders[i]
            next_leader = leaders[i+1]

            cl_in_instructions = instructions.index(current_leader) if current_leader in instructions else -1
            nl_in_instructions = instructions.index(next_leader) if next_leader in instructions else -1

            if i == 0:
                basic_blocks.append(BasicBlock(current_leader, i+1, BasicBlock.BlockType.ROOT))
            elif 'if ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i+1, BasicBlock.BlockType.IF_THEN))
            elif 'elif ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i+1, BasicBlock.BlockType.ELIF))
            elif 'else: ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i+1, BasicBlock.BlockType.ELSE))
            else:
                basic_blocks.append(BasicBlock(current_leader, i+1, BasicBlock.BlockType.ORDINARY))

            if -1 == cl_in_instructions:
                return basic_blocks

            for instruction in instructions[cl_in_instructions: nl_in_instructions]:
                basic_blocks[-1].add_instruction(instruction)

            instructions = instructions[nl_in_instructions:]

        return basic_blocks

    def get_leaders(self, instructions):
        leaders = [instructions[0]]
        control_flow_changers = ['if', 'else', 'elif', 'for']

        num_tabs = 0
        for i in range(len(instructions)):
            instruction = instructions[i]

            function_call_occurs = len(re.findall(r'^(?!def)(\w|\_)+\([\w\s\d|,]*\)', instructions[i].strip(),
                                         re.IGNORECASE))
            num_tabs_prev = num_tabs
            num_tabs = int((len(instruction) - len(instruction.lstrip(' ')))/4)
            if any(cfc in instruction for cfc in control_flow_changers) or 0 != function_call_occurs\
                    or num_tabs_prev > num_tabs:
                if i + 1 != len(instructions):
                    leaders.append(instruction)

        return leaders

    def determine_parents(self, blocks):
        for block in blocks:
            pass