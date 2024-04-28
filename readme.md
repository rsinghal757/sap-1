# SAP-1 Emulator in Python

This repository contains a Python implementation of the Simple As Possible 1 (SAP-1) computer architecture. The SAP-1 is a basic computer architecture designed for educational purposes to understand the fundamental concepts of computer organization and assembly programming.

## Features

- Emulates the SAP-1 architecture with a simple CPU and memory model
- Supports a subset of SAP-1 instructions, including:
  - `LDA`: Load value from memory address to accumulator
  - `ADD`: Add value from memory address to accumulator
  - `SUB`: Subtract value from memory address from accumulator
  - `JNZ`: Jump to memory address if accumulator is not zero
  - `STA`: Store value from accumulator to memory address
  - `HLT`: Halt the program
- Assembler to convert assembly instructions to machine code
- Emulation loop to fetch, decode, and execute instructions
- Example program to calculate the sum of numbers from 1 to N

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/rsinghal757/sap-1.git
   ```

2. Run the emulator:
   ```
   python sap1_emulator.py
   ```

3. Modify the `assembly_program` in the `main()` function to create your own SAP-1 programs.

## Example Program

The provided example program calculates the sum of numbers from 1 to N, where N is stored in memory location 15. The program uses a loop to add each number to the sum, which is stored in memory location 17.

```
LDA 15    # Load N into the accumulator
STA 10    # Store N in memory location 10 (loop counter)
LDA 17    # Load the sum into the accumulator
ADD 10    # Add the current loop counter to the sum
STA 17    # Store the updated sum in memory location 17
LDA 10    # Load the loop counter into the accumulator
SUB 16    # Subtract 1 from the loop counter
STA 10    # Store the updated loop counter in memory location 10
JNZ 2     # Jump to the instruction at memory location 2 if the loop counter is not zero
HLT       # Halt the program
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).