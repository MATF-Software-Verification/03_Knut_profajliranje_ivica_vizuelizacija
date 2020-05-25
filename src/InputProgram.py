from src.blocks.BasicBlock import BasicBlock
import re


class InputProgram:
    def __init__(self, code):
        self.instructions = self.make_instructions(code)
        self.basic_blocks = self.divide_into_basic_blocks(self.instructions)

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

        current_leader = leaders[0]
        next_leader = leaders[1]

        leaders_size = len(leaders)
        for i in range(1, leaders_size):
            cl_in_instructions = instructions.index(current_leader) if current_leader in instructions else -1
            nl_in_instructions = instructions.index(next_leader) if next_leader in instructions else -1

            if i == 0:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.ROOT))
            elif 'for ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.FOR))
            elif 'elif ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.ELIF))
            elif 'if ' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.IF_THEN))
            elif 'else:' in current_leader:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.ELSE))
            elif self.num_function_calls(current_leader) > 0:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.FUNCTION))
            else:
                basic_blocks.append(BasicBlock(current_leader, i, BasicBlock.BlockType.ORDINARY))

            if -1 == cl_in_instructions:
                return basic_blocks

            for instruction in instructions[cl_in_instructions: nl_in_instructions]:
                basic_blocks[-1].add_instruction(instruction)

            instructions = instructions[nl_in_instructions:]

            current_leader = next_leader
            if i < leaders_size - 1:
                next_leader = leaders[i + 1]

        basic_blocks.append(BasicBlock(next_leader, i + 1, BasicBlock.BlockType.ORDINARY))
        nl_in_instructions = instructions.index(next_leader) if next_leader in instructions else -1
        for instruction in instructions[nl_in_instructions:]:
            basic_blocks[-1].add_instruction(instruction)

        return basic_blocks

    def get_leaders(self, instructions):
        leaders = [instructions[0]]
        control_flow_changers = ['if', 'else', 'elif', 'for']

        num_tabs = 0
        for i in range(len(instructions)):
            instruction = instructions[i]

            function_call_occurs = self.num_function_calls(instruction)
            num_tabs_prev = num_tabs
            num_tabs = self.calculate_tabs(instruction)
            if any(cfc in instruction for cfc in control_flow_changers) or 0 != function_call_occurs:
                leaders.append(instruction)
                if i + 1 != len(instructions):
                    leaders.append(instructions[i+1])
            elif num_tabs_prev > num_tabs:
                leaders.append(instruction)

        return leaders

    def determine_parents(self):
        block_matrix = []
        num_tabs = 0
        num_tabs_prev = 0
        with open('blocks.txt', "w+") as output:
            for block in self.basic_blocks:
                if num_tabs_prev > num_tabs and block.type in [BasicBlock.BlockType.ORDINARY,
                                                               BasicBlock.BlockType.FUNCTION, BasicBlock.BlockType.ENDING]:
                    current_block_info = [block.type.name, block.id, num_tabs_prev - num_tabs, False]
                else:
                    current_block_info = [block.type.name, block.id, 0, False]

                block_matrix.append(current_block_info)
                output.write('%s\n' % current_block_info)

                num_tabs_prev = num_tabs
                num_tabs = self.calculate_tabs(block.lead)
        return block_matrix

    def calculate_tabs(self, instruction):
        return int((len(instruction) - len(instruction.lstrip(' '))) / 4)

    def num_function_calls(self, instruction):
        # ^(?!def)
        return len(re.findall(r'(\w|\_)+\([\w\s\d|,]*\)', instruction.strip(), re.IGNORECASE))
