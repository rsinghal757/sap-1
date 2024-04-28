# Define SAP-1 memory size (e.g., 20 bytes)
MEMORY_SIZE = 20

# Define SAP-1 register names
registers = {
    "ACC": 0,  # Accumulator
    "PC": 0,   # Program Counter
}

# Define symbolic opcodes for readability (map to actual hex opcodes)
opcodes = {
    "LDA": 0x1, # Load value from memory address to accumulator
    "ADD": 0x2, # Add value from memory address to accumulator
    "SUB": 0x3, # Subtract value from memory address from accumulator
    "JNZ": 0x4, # Jump to memory address if accumulator is not zero
    "STA": 0x5, # Store value from accumulator to memory address
    "HLT": 0x0, # Halt the program
}

class Memory:
    def __init__(self, size):
        self.memory = ['0'] * size  # Initialize memory with '0' as strings

    def load(self, address):
        return self.memory[address]

    def store(self, address, value):
        self.memory[address] = value

class CPU:
    def __init__(self, memory):
        self.memory = memory

    def fetch(self):
        # Fetch instruction from program counter (PC) address
        instruction = self.memory.load(registers["PC"])
        # Increment program counter for next instruction
        registers["PC"] += 1
        return instruction

    def decode(self, instruction):
        # Extract opcode and operand from instruction based on SAP-1 format
        parts = instruction.split()
        opcode = int(parts[0], 2)
        operand = int(parts[1], 2) if len(parts) > 1 else None
        return opcode, operand

    def execute(self, opcode, operand):
        # Execute the instruction based on opcode and operands
        if opcode == opcodes["LDA"]:
            self.load_accumulator(operand)
        elif opcode == opcodes["ADD"]:
            self.add_to_accumulator(operand)
        elif opcode == opcodes["SUB"]:
            self.subtract_from_accumulator(operand)
        elif opcode == opcodes["JNZ"]:
            self.jump_if_not_zero(operand)
        elif opcode == opcodes["STA"]:
            self.store_accumulator(operand)
        elif opcode == opcodes["HLT"]:
            print("Program Halted!")
        else:
            print(f"Invalid opcode: {opcode}")

    def load_accumulator(self, operand):
        # Load the value from the memory location (operand) into the accumulator register
        registers["ACC"] = self.memory.load(operand)

    def add_to_accumulator(self, operand):
        # Add the value from the memory location (operand) to the accumulator register
        registers["ACC"] += self.memory.load(operand)

    def subtract_from_accumulator(self, operand):
        # Subtract the value from memory location (operand) from the accumulator register
        registers["ACC"] -= self.memory.load(operand)

    def jump_if_not_zero(self, operand):
        # If the accumulator register is not zero, jump to the memory location specified by the operand
        if registers["ACC"] != 0:
            registers["PC"] = operand

    def store_accumulator(self, operand):
        # Store the value from the accumulator register into the memory location specified by the operand
        self.memory.store(operand, registers["ACC"])

class Assembler:
    def assemble(self, program):
        machine_code = []
        for instruction in program:
            # Split instruction (mnemonic and operand)
            parts = instruction.split()
            opcode = opcodes.get(parts[0])  # Get opcode using symbolic name
            if opcode is None:
                raise ValueError(f"Invalid instruction: {instruction}")
            
            # Handle different instruction formats (depending on opcode)
            if len(parts) == 1:  # Instructions without operand (e.g., HLT)
                machine_code.append(bin(opcode))
            elif len(parts) == 2:  # Instructions with operand (e.g., LDA 10)
                try:
                    operand = int(parts[1])  # Try converting operand to decimal
                    if operand < 0 or operand >= MEMORY_SIZE:
                        raise ValueError(f"Invalid operand value: {operand}")
                    machine_code.append(bin(opcode) + " " + bin(operand))  # Combine opcode and operand
                except ValueError:
                    raise ValueError(f"Invalid operand format: {parts[1]}")
            else:
                raise ValueError(f"Invalid instruction format: {instruction}")
        return machine_code

def load_program(memory, program):
    for i, instruction in enumerate(program):
        memory.store(i, instruction)

def main():
    # Initialize memory and CPU objects
    memory = Memory(MEMORY_SIZE)
    cpu = CPU(memory)

    # Define assembly program (Data and Instructions)
    # Assembly data
    memory.store(15, 20)  # N = 5
    memory.store(16, 1)  # Constant 1
    memory.store(17, 0)  # Sum initialized to 0

    # Assembly program
    assembly_program = [
        "LDA 15",   # Load N into the accumulator
        "STA 10",   # Store N in memory location 10 (loop counter)
        "LDA 17",   # Load the sum into the accumulator
        "ADD 10",   # Add the current loop counter to the sum
        "STA 17",   # Store the updated sum in memory location 17
        "LDA 10",   # Load the loop counter into the accumulator
        "SUB 16",   # Subtract 1 from the loop counter
        "STA 10",   # Store the updated loop counter in memory location 10
        "JNZ 2",    # Jump to the instruction at memory location 2 if the loop counter is not zero
        "HLT",      # Halt the program
    ]

    # Assemble the program into machine code
    assembler = Assembler()
    machine_code = assembler.assemble(assembly_program)

    # Load machine code into memory
    load_program(memory, machine_code)

    # Emulation loop
    while True:
        # Fetch instruction
        instruction = cpu.fetch()

        # Decode instruction
        opcode, operand = cpu.decode(instruction)

        # Execute instruction
        cpu.execute(opcode, operand)

        # Check for halt condition
        if opcode == opcodes["HLT"]:
            break

        # # Log state (for debugging)
        # print(f"ACC: {registers['ACC']}")
        # print(f"PC: {registers['PC']}")
        # print(f"Loop Counter: {memory.memory[10]}")
        # print(f"Sum: {memory.memory[17]}")
        # print("-----------------")
        

    print(f"Sum: {memory.memory[17]}")

if __name__ == "__main__":
    main()