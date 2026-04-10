from core import *

def execute_r(inst):
    global PC
    rd, f3, rs1, rs2, f7 = bits(inst,11,7), bits(inst,14,12), bits(inst,19,15), bits(inst,24,20), bits(inst,31,25)

    a, b = s_ext(R[rs1],32), s_ext(R[rs2],32)
    ua, ub = R[rs1], R[rs2]

    if f3 == 0 and f7 == 0:    res = a + b
    elif f3 == 0 and f7 == 32: res = a - b
    elif f3 == 1:              res = ua << (ub & 31)
    elif f3 == 2:              res = 1 if a < b else 0
    elif f3 == 3:              res = 1 if ua < ub else 0
    elif f3 == 4:              res = ua ^ ub
    elif f3 == 5 and f7 == 0:  res = ua >> (ub & 31)
    elif f3 == 6:              res = ua | ub
    elif f3 == 7:              res = ua & ub
    else: return f"Error: Unknown R-type funct3={f3} funct7={f7} at PC={PC:#010x}"

    write_reg(rd, res)
    PC += 4
    return None


def execute_i(inst):
    global PC
    rd, f3, rs1 = bits(inst,11,7), bits(inst,14,12), bits(inst,19,15)
    imm = s_ext(bits(inst,31,20),12)

    val = s_ext(R[rs1],32)
    uval = R[rs1]

    if f3 == 0:   write_reg(rd, val + imm)
    elif f3 == 3: write_reg(rd, 1 if uval < (imm & 0xFFF) else 0)
    else: return f"Error: Unknown I-type funct3={f3} at PC={PC:#010x}"

    PC += 4
    return None


def execute_lw(inst):
    global PC
    rd, rs1 = bits(inst,11,7), bits(inst,19,15)
    imm = s_ext(bits(inst,31,20),12)

    addr = u32(R[rs1] + imm)
    err = check_mem_access(addr, "lw")
    if err: return err

    write_reg(rd, read_mem(addr))
    PC += 4
    return None


def execute_sw(inst):
    global PC
    rs1, rs2 = bits(inst,19,15), bits(inst,24,20)
    imm = s_ext((bits(inst,31,25)<<5)|bits(inst,11,7),12)

    addr = u32(R[rs1] + imm)
    err = check_mem_access(addr, "sw")
    if err: return err

    write_mem(addr, R[rs2])
    PC += 4
    return None
