import sys

# Register file and memory
registers = [0] * 32
memory = [0] * 256  # 128 for instructions and 128 for data

def load_registers_from_file(filename):
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if line.strip():
                    registers[i] = int(line.strip(), 16)
    except Exception as e:
        print(f"Error loading registers from file: {e}")

def load_memory_from_file(filename):
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if line.strip():
                    memory[i] = int(line.strip(), 16)
    except Exception as e:
        print(f"Error loading memory from file: {e}")

def load_program_from_file(filename):
    program = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    program.append(int(line.strip(), 16))  # Assuming the program file contains hex instructions
    except Exception as e:
        print(f"Error loading program from file: {e}")
    return program

def load_instruction(address):
    # Load instruction from memory
    return memory[address // 4]

def execute_instruction(instruction, results_file, mode):
    opcode = instruction >> 26
    rs = (instruction >> 21) & 0x1F
    rt = (instruction >> 16) & 0x1F
    rd = (instruction >> 11) & 0x1F
    shamt = (instruction >> 6) & 0x1F
    funct = instruction & 0x3F
    instr_type = ""
    operation = ""
    relevant_registers = {}
    relevant_memory = {}

    try:
        if opcode == 0:  # R-Type
            instr_type = "R-Type"
            if funct == 32:  # add
                registers[rd] = registers[rs] + registers[rt]
                operation = "add"
                relevant_registers = {rs: registers[rs], rt: registers[rt], rd: registers[rd]}
            elif funct == 34:  # sub
                registers[rd] = registers[rs] - registers[rt]
                operation = "sub"
                relevant_registers = {rs: registers[rs], rt: registers[rt], rd: registers[rd]}
            elif funct == 36:  # and
                registers[rd] = registers[rs] & registers[rt]
                operation = "and"
                relevant_registers = {rs: registers[rs], rt: registers[rt], rd: registers[rd]}
            elif funct == 37:  # or
                registers[rd] = registers[rs] | registers[rt]
                operation = "or"
                relevant_registers = {rs: registers[rs], rt: registers[rt], rd: registers[rd]}
            elif funct == 0:  # sll
                registers[rd] = registers[rt] << shamt
                operation = "sll"
                relevant_registers = {rt: registers[rt], rd: registers[rd]}
            elif funct == 2:  # srl
                registers[rd] = registers[rt] >> shamt
                operation = "srl"
                relevant_registers = {rt: registers[rt], rd: registers[rd]}
                print("executing srl")
            else:
                raise ValueError("Illegal R-Type function")
        elif opcode == 35:  # lw (load word)
            instr_type = "I-Type"
            address = (registers[rs] + (instruction & 0xFFFF)) // 4
            registers[rt] = memory[address]
            operation = "lw"
            relevant_registers = {rs: registers[rs], rt: registers[rt]}
            relevant_memory = {address: memory[address]}
            print("executing lw")
        elif opcode == 43:  # sw (store word)
            instr_type = "I-Type"
            address = (registers[rs] + (instruction & 0xFFFF)) // 4
            memory[address] = registers[rt]
            operation = "sw"
            relevant_registers = {rs: registers[rs], rt: registers[rt]}
            relevant_memory = {address: registers[rt]}
            print("executing sw")
        elif opcode == 2:  # j (jump)
            print("executing j")
            instr_type = "J-Type"
            address = instruction & 0x3FFFFFF
            #write to file
            with open(results_file, 'a') as f:
                f.write(f"Instruction: 0x{instruction:08X}, Type: {instr_type}, Operation: j\n")
                f.write("\n")
            return address * 4
        elif opcode == 4:  # beq (branch if equal)
            print("executing beq")
            instr_type = "I-Type"
            relevant_registers = {rs: registers[rs], rt: registers[rt]}
            if registers[rs] == registers[rt]:
                offset = (instruction & 0xFFFF)
                if offset & 0x8000:  # negative offset
                    offset -= 0x10000
                return offset * 4
        else:
            raise ValueError("Illegal Opcode")
    except Exception as e:
        if mode == "Single_Step":
            print(f"Error: {e}")

    # Write relevant details to the file during "Run_All" mode
    if instr_type:  # Only write if instruction type exists
        with open(results_file, 'a') as f:
            f.write(f"Instruction: 0x{instruction:08X}, Type: {instr_type}, Operation: {operation}\n")
            f.write("Relevant register values:\n")
            for reg, val in relevant_registers.items():
                f.write(f"$r{reg} (Address {reg}): {val}\n")
            if relevant_memory:
                f.write("Relevant memory values:\n")
                for addr, val in relevant_memory.items():
                    f.write(f"Memory[{addr}] (Address {addr*4}): {val}\n")
            f.write("\n")

    return None


def run_program(program, results_file, mode):
    pc = 0
    while pc < len(program):
        instruction = program[pc]
        offset = execute_instruction(instruction, results_file, mode)
        if offset is not None:
            pc += offset
        else:
            pc += 1
        if mode == "Single_Step":
            choice = ""
            while True:
                print(f"PC: {pc}, Instruction: 0x{instruction:08X}, Registers: {registers}")
                choice = input("Press Enter to execute next instruction, or 'q' to quit: ")
                if choice == 'q':
                    sys.exit(0)
                elif choice == "":
                    break
                else:
                    print("Invalid input. Please try again.")
   
    # Print final register values and memory contents
    if mode == "Run_All":
        print("Final Register Values:")
        for i, val in enumerate(registers):
            print(f"R{i}: {val}")
        
        print("\nFinal Memory Contents:")
        for i, val in enumerate(memory):
            print(f"Memory[{i*4}]: {val}")


def main():
    # Initialize files and mode
    reg_init_file = "Reg_Init_File.txt"
    mem_init_file = "Mem_Init_File.txt"
    results_file = "results.txt"
    
    load_registers_from_file(reg_init_file)
    load_memory_from_file(mem_init_file)
    
    program_file = input("Enter the program file name (e.g., Program.asm): ")
    program = load_program_from_file(program_file)
    
    mode = input("Enter mode (Single_Step or Run_All): ")
    
    with open(results_file, 'w') as f:
        f.write("MIPS Simulation Results\n\n")  # Clear the file and write header
    
    run_program(program, results_file, mode)
    print(f"Simulation complete. Results written to {results_file}")

if __name__ == "__main__":
    main()
