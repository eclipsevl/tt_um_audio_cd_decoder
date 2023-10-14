# RS(15,11) encoder, textbook example
# Vladislav Knyazkov, October 2023
import random

# RS(15, 11)
# GF(2^4 = 16)
# Primitive polynomial: x^4 + x + 1
# Generator polynomial: x^4 + 15x^3 + 3x^2 + x + 12
n = 32
k = 28
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

def gf_inv(a):
    if(a==0):
        print("Error! Div by 0")
    for i in range(2**gfm):
        if(gf_mult(a, i) == 1):
            return i
    
    return 0

def eclid_alg(s3, s2, s1, s0, verbose = 0):
    # euclidian algorithm
    if(verbose):
        print(f"step:\ta3\ta2\ta1\ta0\tb3\tb2\tb1\tb0")
    # step 1 - initial conditions

    # register a: load syndrome
    if(s3 > 0):
        a0 = s0
        a1 = s1
        a2 = s2
        a3 = s3
    else:
        a0 = 0
        a1 = s0
        a2 = s1
        a3 = s2 

        if(s2 == 0):
            print(f"s3={s3}, s2={s2},s1={s1}, s0={s0}")       

   
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
    
    if(verbose):
        print(f"1:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")


    if(s3 == 0):
        # step 1.5 - calc and load results into reg b 
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

        sd0 = gf_add(d0, 0)# WTF moment! mult by 10x
        sd1 = gf_add(d1, 0)
        sd2 = gf_add(d2, mc0)

        d0 = sd0
        d1 = sd1
        d2 = sd2

        if(verbose):
            print(f"Substract {ma3}x, residue {b3}x3 + {b2}x2 + {b1}x + {b0}")
            print(f"2:\t{a3}\t{a2}\t{a1}\t{a0}\t{b3}\t{b2}\t{b1}\t{b0}\t{c1}\t{c0}\t{d2}\t{d1}\t{d0}")


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

    sd0 = gf_add(d0, 0)# WTF moment! mult by 10x
    sd1 = gf_add(d1, mc0)
    sd2 = gf_add(d2, mc1)

    d0 = sd0
    d1 = sd1
    d2 = sd2

    if(verbose):
        print(f"Substract {ma3}x, residue {b3}x3 + {b2}x2 + {b1}x + {b0}")
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

    mc0 = gf_mult(c0, ma3)
    mc1 = gf_mult(c1, ma3)

    sd0 = gf_add(d0, mc0)# WTF moment! mult by 6
    sd1 = gf_add(d1, mc1)
    sd2 = gf_add(d2, 0)

    d0 = c0
    d1 = c1
    d2 = 0

    c0 = sd0
    c1 = sd1

    if(a3 > 0 and s3 > 0):
        if(verbose):
            print(f"Substract {ma3}, residue {a3}x2 + {a2}x1 + {a1}")
            print(f"Residual degree: 2, continue")
    else:
        if(verbose):
            print(f"Substract {ma3}, residue {a3}x2 + {a2}x1 + {a1}")
            print(f"Residual degree: < 2, need to stop")

        if(s3 > 0):
            gO0 = sb0 # WTF moment!
            gO1 = sb1
        else:
            gO0 = sb1 # WTF moment!
            gO1 = sb2

        gG0 = sd0
        gG1 = sd1
        gG2 = sd2
        
        if(verbose):
            print(f"Res: ({gG2}x2 + {gG1}x  + {gG0}) + ({gO1}x  + {gO0})")
        return [gO1, gO0, gG2, gG1, gG0]

    # top
    if(verbose):
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

    sd0 = gf_add(d0, 0)# WTF moment! mult by 2x
    sd1 = gf_add(d1, mc0)
    sd2 = gf_add(d2, mc1)

    d0 = sd0
    d1 = sd1
    d2 = sd2

    if(verbose):
        if(verbose):
            print(f"Substract {ma3}, residue {a3}x2 + {a2}x1 + {a1}")
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

    sd0 = gf_add(d0, mc0)# WTF moment!
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

    if(verbose):
        if(verbose):
            print(f"Substract {ma3}, residue {a3}x2 + {a2}x1 + {a1}")
        print(f"Res: ({gG2}x2 + {gG1}x  + {gG0}) + ({gO1}x  + {gO0})")

    return [gO1, gO0, gG2, gG1, gG0]

if __name__ == "__main__":
    print("12,4,3,15")
    eclid_alg(12,4,3,15, 1)

    print("7,2,11,13")
    eclid_alg(7,2,11,13, 1)

    print("16,4,2,1")
    eclid_alg(0,4,2,1, 1)