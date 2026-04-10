# decoder.py

from core import *

def get_opcode(inst):
    return bits(inst, 6, 0)

def is_halt(inst):
    op = get_opcode(inst)
    if op == 0b1100011:
        rs1 = bits(inst,19,15)
        rs2 = bits(inst,24,20)
        imm = s_ext((bits(inst,31,31)<<12)|(bits(inst,7,7)<<11)|
                    (bits(inst,30,25)<<5)|(bits(inst,11,8)<<1),13)
        return rs1 == 0 and rs2 == 0 and imm == 0
    return False
