# RS(15,11) encoder, textbook example
# Vladislav Knyazkov, October 2023

def gf_add(a, b):
    return a ^ b

def gf_mult(x,y):
    p = 0b10011      #  modulo x^4 + x + 1
    m = 0            # m will be product
    for i in range(4):
        m = m << 1
        if m & 0b10000:
            m = m ^ p
        if y & 0b01000:
            m = m ^ x
        y = y << 1
    return m

def gf_inv(a):
    for i in range(16):
        if(gf_mult(a, i) == 1):
            return i
    
    return 0
# GF(16)
# Primitive polynomial: x^4 + x + 1
# Generator polynomial: x^4 + 15x^3 + 3x^2 + x + 12

# Encoder hardware implementation
def encode(MX):
    TX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # clock cycle counter
    cntr = 0

    # encoder registers
    reg0 = 0
    reg1 = 0
    reg2 = 0
    reg3 = 0

    while(cntr < 15):
        control = cntr < 11    

        # and gate
        if(control == 1):
            # Phase 1: loading the message
            TX[cntr] = MX[cntr]
            and_out = gf_add(reg3, MX[cntr])
        else: 
            # phase 2: shift out RX
            TX[cntr] = reg3
            and_out = 0

        # multipliers
        m0 = gf_mult(and_out, 12)
        m1 = gf_mult(and_out, 1)
        m2 = gf_mult(and_out, 3)
        m3 = gf_mult(and_out, 15)

        # adders
        s0 = gf_add(reg0, m1)
        s1 = gf_add(reg1, m2)
        s2 = gf_add(reg2, m3)
        #s3 = gf_add(reg3, and_out)

        # registers
        reg0 = m0
        reg1 = s0
        reg2 = s1
        reg3 = s2    

        cntr = cntr + 1
    
    return TX

def add_error(TX, EX):
    _RX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 15):
        _RX[i] = TX[i]^EX[i]

    return _RX

def decode(RX):
    DX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # calculate syndrome
    reg0 = 0
    reg1 = 0
    reg2 = 0
    reg3 = 0

    cntr = 0
    while(cntr < 15):   
        # There was a mistake in the textbook!
        s0 = gf_add(reg0, RX[cntr-15])
        m0 = gf_mult(s0, 1)
        reg0 = m0

        s1 = gf_add(reg1, RX[cntr-15])
        m1 = gf_mult(s1, 2)
        reg1 = m1

        s2 = gf_add(reg2, RX[cntr-15])
        m2 = gf_mult(s2, 4)
        reg2 = m2
    
        s3 = gf_add(reg3, RX[cntr-15])
        m3 = gf_mult(s3, 8)
        reg3 = m3
        #print(f"({reg0} + {RX[cntr-15]}) * 8 = {m0}")        

        cntr = cntr + 1

    #s0 = reg0
    print(f"syndrome: {s3, s2, s1, s0}")

    # euclidian algorithm
    print(f"step:\ta3\ta2\ta1\ta0\tb3\tb2\tb1\tb0")
    # step 1 - initial conditions

    # register a: load syndrome
    a0 = s0
    a1 = s1
    a2 = s2
    a3 = s3

    # register b: X^4
    b0 = 0
    b1 = 0
    b2 = 0
    b3 = 1

    # register c: 1
    c0 = 1
    c1 = 0

    # register d: 0
    d0 = 0
    d1 = 0
    d2 = 0
    
    print(f"1:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")

    # step 2 - calc and load results into reg b
    a3_inv = gf_inv(a3)
    ma3 = gf_mult(a3_inv, b3)

    ma0 = gf_mult(a0, ma3)
    ma1 = gf_mult(a1, ma3)
    ma2 = gf_mult(a2, ma3)

    sb0 = gf_add(b0, ma0)
    sb1 = gf_add(b1, ma1)
    sb2 = gf_add(b2, ma2)

    b0 = 0
    b1 = sb0
    b2 = sb1
    b3 = sb2

    #top
    mc0 = gf_mult(c0, ma3)
    mc1 = gf_mult(c1, ma3)

    sd0 = gf_add(d0, 0)
    sd1 = gf_add(d1, mc0)
    sd2 = gf_add(d2, mc1)

    d0 = sd0
    d1 = sd1
    d2 = sd2

    print(f"2:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")

    # step 3: load a -> b, calc results -> a
    a3_inv = gf_inv(a3)
    ma3 = gf_mult(a3_inv, b3)

    ma0 = gf_mult(a0, ma3)
    ma1 = gf_mult(a1, ma3)
    ma2 = gf_mult(a2, ma3)

    sb0 = gf_add(b0, ma0)
    sb1 = gf_add(b1, ma1)
    sb2 = gf_add(b2, ma2)

    b0 = a0
    b1 = a1
    b2 = a2
    b3 = a3

    a0 = 0
    a1 = sb0
    a2 = sb1
    a3 = sb2

    # top
    mc0 = gf_mult(c0, ma3)
    mc1 = gf_mult(c1, ma3)

    sd0 = gf_add(d0, mc0)
    sd1 = gf_add(d1, mc1)
    sd2 = gf_add(d2, 0)

    d0 = c0
    d1 = c1
    d2 = 0

    c0 = sd0
    c1 = sd1

    print(f"3:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")

    # step 4 - repeat step 2
    a3_inv = gf_inv(a3)
    ma3 = gf_mult(a3_inv, b3)

    ma0 = gf_mult(a0, ma3)
    ma1 = gf_mult(a1, ma3)
    ma2 = gf_mult(a2, ma3)

    sb0 = gf_add(b0, ma0)
    sb1 = gf_add(b1, ma1)
    sb2 = gf_add(b2, ma2)

    b0 = 0
    b1 = sb0
    b2 = sb1
    b3 = sb2

    #top
    mc0 = gf_mult(c0, ma3)
    mc1 = gf_mult(c1, ma3)

    sd0 = gf_add(d0, 0)
    sd1 = gf_add(d1, mc0)
    sd2 = gf_add(d2, mc1)

    d0 = sd0
    d1 = sd1
    d2 = sd2

    print(f"4:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")

    a3_inv = gf_inv(a3)
    ma3 = gf_mult(a3_inv, b3)

    ma0 = gf_mult(a0, ma3)
    ma1 = gf_mult(a1, ma3)
    ma2 = gf_mult(a2, ma3)

    sb0 = gf_add(b0, ma0)
    sb1 = gf_add(b1, ma1)
    sb2 = gf_add(b2, ma2)

    # top
    mc0 = gf_mult(c0, ma3)
    mc1 = gf_mult(c1, ma3)

    sd0 = gf_add(d0, mc0)
    sd1 = gf_add(d1, mc1)
    sd2 = gf_add(d2, 0)

    d0 = c0
    d1 = c1
    d2 = 0

    c0 = sd0
    c1 = sd1

    gO0 = sb1
    gO1 = sb2

    gG0 = sd0
    gG1 = sd1
    gG2 = sd2

    print(f"Error mag poly: [{gO1}, {gO0}]")
    print(f"Error loc poly: [{gG1}, {gG1}, {gG0}]")
 

    # the Chien search
    csr0 = gf_mult(gG0, 1)
    csr1 = gf_mult(gG1, 2)
    csr2 = gf_mult(gG2, 4)

    # error correction
    ecr0 = gf_mult(gO0, 1)
    ecr1 = gf_mult(gO1, 2)

    ksi = 0

    err_pos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    err_val = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    cntr = 0
    while(cntr < 15):   
        # search error location regs
        csm0 = gf_mult(csr0, 1)
        csm1 = gf_mult(csr1, 2)
        csm2 = gf_mult(csr2, 4)

        # error correctio regs
        ecm0 = gf_mult(ecr0, 1)
        ecm1 = gf_mult(ecr1, 2)

        if(gf_add(csr0, gf_add(csr1, csr2)) == 0):
            err_pos[cntr] = 1
            ksi = csr1

            evs = gf_add(ecr0, ecr1)
            err_val[cntr] = gf_mult(evs, gf_inv(ksi))

        csr0 = csm0
        csr1 = csm1
        csr2 = csm2

        ecr0 = ecm0
        ecr1 = ecm1

        DX[cntr] = RX[cntr] ^ err_val[cntr]

        cntr = cntr + 1

    print(f"Error locations: {err_pos}")
    print(f"Error values: {err_val}")

    return DX


# Message polynomial
MX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
EX = [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
RX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

TX = encode(MX)
RX = add_error(TX, EX)

DX = decode(RX)

print(MX)
print(TX)
print(RX)
print(DX)

if(TX == DX):
    print("Corrected!")
else:
    print("FAIL!")




