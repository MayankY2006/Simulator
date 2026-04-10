import sys
from core import *
from alu_memory import *
from control import *
from decoder import *

def simulate(out_file):
    global PC
    out = []

    while True:
        if PC < 0 or PC >= len(PROG) * 4:
            print(f"Error: PC {PC:#010x} out of bounds")
            return

        inst = int(PROG[PC//4], 2)
        opcode = get_opcode(inst)

        if is_halt(inst):
            out.append(dump_state())
            with open(out_file, 'w') as f:
                for line in out:
                    f.write(line + "\n")
            return

        if opcode == 0b0110011:
            err = execute_r(inst)
        elif opcode == 0b0010011:
            err = execute_i(inst)
        elif opcode == 0b0000011:
            err = execute_lw(inst)
        elif opcode == 0b0100011:
            err = execute_sw(inst)
        elif opcode == 0b1100011:
            err = execute_branch(inst)
        elif opcode == 0b1101111:
            err = execute_jal(inst)
        elif opcode == 0b1100111:
            err = execute_jalr(inst)
        elif opcode in (0b0110111, 0b0010111):
            err = execute_u(inst, opcode)
        else:
            print("Unknown opcode")
            return

        if err:
            print(err)
            return

        out.append(dump_state())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    R[2] = STACK_TOP
    load_prog(sys.argv[1])
    simulate(sys.argv[2])
