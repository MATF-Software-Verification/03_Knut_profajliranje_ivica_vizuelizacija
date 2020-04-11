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

    def getLead(self):
        return self.lead

    def __str__(self):
        str = ""
        str = "-----------\n"
        for instr in self.instructions:
            if(instr != ""):
                str += instr + "\n"
        str += "-----------"
        return str