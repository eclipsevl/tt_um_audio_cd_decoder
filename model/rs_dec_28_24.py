from rs_enc_dec_32_28 import decode


poly = 0b100011101
gfm = 8

def gf_add(a, b):
    return a ^ b

def gf_mult(x,y):

    p = poly      #  modulo x^4 + x + 1
    m = 0            # m will be product
    for i in range(gfm):
        m = m << 1
        if m & 0b100000000:
            m = m ^ p
        if y & 0b010000000:
            m = m ^ x
        y = y << 1
    return m
    
def calc_parity_c2(_c2_frame):
    s0 = 0
    s1 = 0
    a1 = 1
    s2 = 0
    a2 = 1

    s3 = 0
    a3 = 1

    #frames_c1[j] = [254, 182, 6, 40, 6, 116, 0, 164, 2, 51, 0, 104, 203, 64, 173, 146, 11, 28, 145, 162, 6, 54, 5, 0, 15, 28, 5, 169, 67, 188, 98, 110]
    for i in range(28):
        s0 = gf_add(_c2_frame[i], s0)
        s1 = gf_add(gf_mult(_c2_frame[27-i],a1), s1)
        a1 = gf_mult(a1, 2)

        s2 = gf_add(gf_mult(_c2_frame[27-i],a2), s2)
        a2 = gf_mult(a2, 4)

        s3 = gf_add(gf_mult(_c2_frame[27-i],a3), s3)
        a3 = gf_mult(a3, 4)

    return [s0,s1,s2,s3]

RX = [17, 175, 9, 129, 252, 76, 17, 193, 9, 148, 252, 95, 30, 41, 52, 142, 239, 109, 253, 67, 253, 231, 239, 128, 253, 86, 253, 250, 0, 0, 0, 0]
DX = decode(RX, 1)

print(RX)
print(DX)