IMEM_START = 0x00000000
DMEM_START = 0x00010000
STACK_TOP = 0x0000017C

PROG_MEM_START  = 0x00000000
PROG_MEM_END    = 0x000000FF
STACK_MEM_START = 0x00000100
STACK_MEM_END   = 0x0000017F
DATA_MEM_START  = 0x00010000
DATA_MEM_END    = 0x0001007F

R = [0] * 32
PC = 0
MEM = {}
PROG = []

def s_ext(val, bits):
    if val >= (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def u32(val):
    return val & 0xFFFFFFFF

def bin32(val):
    return "0b" + format(u32(val), '032b')

def bits(x, hi, lo):
    return (x >> lo) & ((1 << (hi - lo + 1)) - 1)

def read_mem(addr):
    return MEM.get(addr, 0)

def write_mem(addr, val):
    MEM[addr] = u32(val)

def write_reg(i, val):
    if i != 0:
        R[i] = u32(val)

def load_prog(path):
    global PROG
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                PROG.append(line)
    for i, ins in enumerate(PROG):
        MEM[IMEM_START + i * 4] = int(ins, 2)

def check_mem_access(address, op):
    if address % 4 != 0:
        return f"Error: Misaligned memory access at address 0x{address:08X} for {op}"
    in_stack = STACK_MEM_START <= address <= STACK_MEM_END
    in_data  = DATA_MEM_START  <= address <= DATA_MEM_END
    in_prog  = PROG_MEM_START  <= address <= PROG_MEM_END
    if not (in_stack or in_data or in_prog):
        return f"Error: Memory access out of range at address 0x{address:08X} for {op}"
    return None

def dump_state():
    return " ".join([bin32(PC)] + [bin32(x) for x in R]) + " "
