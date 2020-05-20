class BasicBlock:
    def __init__(self, lead):
        self.lead = lead
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def get_instructions(self):
        return self.instructions

    def set_instructions(self, instructions):
        self.instructions = instructions

    def get_lead(self):
        return self.lead

    def stringify_block(self, block_id):
        block_type = ''
        for instr in self.instructions:
            if instr.find('if ') != -1:
                block_type = 'if then'
                break
            elif instr.find('else ') != -1:
                block_type = 'else'
                break
            elif instr.find('elif ') != -1:
                block_type = 'elif'
                break
            elif instr.find('for ') != -1:
                block_type = 'for'
                break
            else:
                block_type = 'ordinary'
                
        ret_str = f"# -BEGIN BLOCK id: {block_id} type: {block_type} parents: {'TODO'}\n"
        for instr in self.instructions:
            if instr != "":
                ret_str += instr + "\n"
        ret_str += f"# -END BLOCK id: {block_id}"
        
        return ret_str
