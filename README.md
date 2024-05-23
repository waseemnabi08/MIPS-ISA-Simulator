## MIPS ISA Simulator

This repository contains a user-friendly MIPS Instruction Set Architecture (ISA) simulator written in Python. It's designed to aid you in understanding and debugging MIPS assembly language programs.

**Features**

* **Supports core MIPS instructions:** Execute R-Type (arithmetic/logic), I-Type (data transfer), and J-Type (control flow) instructions.
* **Flexible execution modes:** Choose between single-stepping through the program or running it entirely.
* **Detailed output:**
    * Single-Step mode: View program counter (PC), disassembled instruction, current register values, and pause to examine the state.
    * Run-All mode: Generate a results file containing instruction details, relevant register values before/after execution, and affected memory locations (for load/store operations).
* **Easy file handling:**
    * Load initial register values from a text file (`Reg_Init_File.txt`).
    * Load program instructions from a separate text file containing hexadecimal instructions (`Program.asm`).
    * Store simulation results in a designated file (`results.txt`).

**Benefits**

* **Enhanced learning:** Gain a deeper understanding of MIPS assembly by observing how instructions manipulate registers and memory.
* **Effective debugging:** Isolate errors in your MIPS programs by pinpointing the problematic instruction.
* **Simplified testing:** Verify the correctness of your MIPS code by running it through the simulator.

**Getting Started**

1. Clone this repository.
2. Install Python ([https://www.python.org/downloads/](https://www.python.org/downloads/)).
3. Edit file paths for `reg_init_file`, `mem_init_file`, and `results_file` in `main.py` if necessary.
4. Place your MIPS assembly language program (in hexadecimal format) in a file named `Program.asm`.
5. Run the simulator from the command line using `python main.py`.
6. Choose the desired execution mode (`Single_Step` or `Run_All`).

**Additional Notes**

* Consider contributing by adding support for more MIPS instructions or features.
* Explore graphical interfaces or visualization tools to enhance the user experience.
* Provide clear instructions on how to create valid MIPS assembly language programs for testing with the simulator (if applicable).
