"""CPU functionality."""

import sys

# Variables per Kenneth suggestion.
# HLT: halt the CPU and exit the emulator.
HLT = 0b00000001
# LDI: load "immediate", store a value in a register, or "set this register to this value".
LDI = 0b10000010
# MUL: Multiply values and store in the first register
MUL = 0b10100010
# POP: Gets the value from memory at the stack pointer
POP = 0b01000110
# PRN: Prints the value at a specific register
PRN = 0b01000111
# PUSH: Push/pop you know the drill
PUSH = 0b01000101
#SPRINT ALU COMMANDS
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):

        # Ram
        self.ram = [0] * 256

        # Eight regs in the register
        self.reg = [0] * 8

        # The program counter
        #self.PC = 0
        self.PC = self.reg[0]

        self.FL = self.reg[4]
        self.SP = self.reg[7]
        self.SP = 7






        # These are the commands that handle how operations are.... handled.
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b10100010: self.mul,
            0b01000110: self.pop,
            0b01000111: self.prn,
            0b01000101: self.push,
            # SPRINT COMMANDS
            0b10100111: self.cmp_func,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
        }

    def cmp_func(self, operand ):

    def ram_read(self, memaddr):
        return self.ram[memaddr]

    def ram_write(self, value, memaddr):
        self.ram[memaddr] = value


    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    split = line.split("#")
                    number = split[0].strip()
                    if number == "":
                        continue
                    value = int(number, 2)

                    self.ram_write(value, address)

                    address += 1
        except FileNotFoundError:
            print(f"{program} program was not found")
            sys.exit(2)

        if len(sys.argv) != 2:
            print("Reformat command: python3 ls8.py <filename>", file=sys.stderr)
            sys.exit(1)

    def ldi(self, oper_a, oper_b):
        self.reg[oper_a] = oper_b
        return 3, True

    def hlt(self, op_a, op_b):
        return 0, False

    def mul(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        return 3, True

    def pop(self, op_a, op_b):
        value = self.ram_read(self.SP)

        self.reg[op_a] = value

        self.SP += 1

        return 2, True

    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        return 2, True

    def push(self, op_a, op_b):
        self.SP -= 1
        value = self.reg[op_a]
        self.ram_write(value, self.SP)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
            return 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True
        while running:

            IR = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)

            try:
                op_output = self.commands[IR](op_a, op_b)

                running = op_output[1]
                self.PC += op_output[0]

            except:
                print(f"Not recognized: {IR}")
                sys.exit(1)


