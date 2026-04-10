from core import *

def execute_branch(inst):
    global PC
    rs1, rs2 = bits(inst,19,15), bits(inst,24,20)
    f3 = bits(inst,14,12)

    imm = s_ext((bits(inst,31,31)<<12)|(bits(inst,7,7)<<11)|
                (bits(inst,30,25)<<5)|(bits(inst,11,8)<<1),13)

    a, b = s_ext(R[rs1],32), s_ext(R[rs2],32)

    take = False
    if f3 == 0:   take = (a == b)
    elif f3 == 1: take = (a != b)
    elif f3 == 4: take = (a < b)
    elif f3 == 5: take = (a >= b)
    elif f3 == 6: take = (R[rs1] < R[rs2])
    elif f3 == 7: take = (R[rs1] >= R[rs2])

    PC = u32(PC + imm) if take else PC + 4
    return None


def execute_jal(inst):
    global PC
    rd = bits(inst,11,7)
    imm = s_ext((bits(inst,31,31)<<20)|(bits(inst,19,12)<<12)|
                (bits(inst,20,20)<<11)|(bits(inst,30,21)<<1),21)

    write_reg(rd, PC+4)
    PC = u32(PC + imm)
    return None


def execute_jalr(inst):
    global PC
    rd, rs1 = bits(inst,11,7), bits(inst,19,15)
    imm = s_ext(bits(inst,31,20),12)

    temp = PC + 4
    PC = u32(R[rs1] + imm) & ~1
    write_reg(rd, temp)
    return None


def execute_u(inst, opcode):
    global PC
    rd = bits(inst,11,7)

    if opcode == 0b0110111:
        write_reg(rd, bits(inst,31,12)<<12)
    else:
        write_reg(rd, PC + (bits(inst,31,12)<<12))

    PC += 4
    return None
