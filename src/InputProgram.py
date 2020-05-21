from src.blocks.BasicBlock import BasicBlock
import re


class InputProgram:
    def __init__(self, code):
        self.instructions = self.make_instructions(code)
        self.basic_blocks = []

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
            elif 'else: ' in current_leader:
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
        # TODO: not working properly yet, fix errors
        blocks_size = len(self.basic_blocks)
        for i in range(blocks_size):
            block = self.basic_blocks[i]
            b_type = block.get_type()
            b_id = block.get_id()

            if b_type in [BasicBlock.BlockType.ROOT, BasicBlock.BlockType.ORDINARY]:
                self.basic_blocks[i + 1].parents.add(b_id) if i + 1 < blocks_size else -1
            elif b_type in [BasicBlock.BlockType.IF_THEN, BasicBlock.BlockType.ELIF, BasicBlock.BlockType.ELSE]:
                self.basic_blocks[i + 1].parents.add(b_id) if i + 1 < blocks_size else -1
                self.basic_blocks[i + 2].parents.add(b_id) if i + 2 < blocks_size else -1

            if b_type == BasicBlock.BlockType.IF_THEN:
                try:
                    next_else = next(block.get_id() for block in self.basic_blocks[i+2:] if block.get_type() == BasicBlock.BlockType.ELSE) \
                        if i + 2 < blocks_size else None
                    first_non_conditional_block = next_else + 2 if next_else + 2 < blocks_size \
                        else next(block.get_id() for block in self.basic_blocks[i+2:] if block.get_type() != BasicBlock.BlockType.IF_THEN)
                    if first_non_conditional_block is not None:
                        for block in self.basic_blocks[i+2:self.basic_blocks.index(first_non_conditional_block)]:
                            if block.get_type() in [BasicBlock.BlockType.ELIF, BasicBlock.BlockType.ELSE]:
                                block.parents.add(b_id)
                except:
                    pass

            try:
                if b_type == BasicBlock.BlockType.FOR:
                    first_non_loop_block = next(block for block in self.basic_blocks[i+2:] if block.get_type() !=
                                                       BasicBlock.BlockType.FOR) if i + 2 < blocks_size else None
                    if first_non_loop_block is not None:
                        first_non_loop_block.parents.add(b_id)
            except:
                pass

            if i < blocks_size - 1:
                next_block = self.basic_blocks[i + 1]
                if self.calculate_tabs(self.basic_blocks[i].get_lead()) < self.calculate_tabs(next_block.get_lead()):
                    next_block.parents.add(b_id)

        return

    def calculate_tabs(self, instruction):
        return int((len(instruction) - len(instruction.lstrip(' '))) / 4)

    def num_function_calls(self, instruction):
        # ^(?!def)
        return len(re.findall(r'(\w|\_)+\([\w\s\d|,]*\)', instruction.strip(), re.IGNORECASE))
