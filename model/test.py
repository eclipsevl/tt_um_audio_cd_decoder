n = 32
k = 28
poly = 0b100011101
gfm = 8
#gen_poly = [64, 120, 70, 15, 1]
gen_poly = [116, 231, 216, 30, 1]


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
            print(f"inv({a}) = {i}")
            return i
    
    return 0

def gf_add(a, b):
    return a ^ b

def eval_poly(p, x):
    x_2 = gf_mult(x,x)
    x_3 = gf_mult(x,x_2)
    x_4 = gf_mult(x,x_3)

    res = gf_mult(p[4], x_4)
    res = gf_add(res, gf_mult(p[3], x_3))
    res = gf_add(res, gf_mult(p[2], x_2))
    res = gf_add(res, gf_mult(p[1], x))
    res = gf_add(res, p[0])

    return res



p = [64,120,54,15,1]
#print(eval_poly(p,1))
#print(eval_poly(p,2))
#print(eval_poly(p,4))
#print(eval_poly(p,8))



m=gf_mult(gf_inv(160),144)
print(m)
print(gf_mult(m,160))
print(gf_mult(m,12))
print(gf_mult(m,142))
print(gf_mult(m,72))

a0s = 1
a1s = 2
a2s = 4
for i in range(223):
    a0s = gf_mult(a0s,1)
    a1s = gf_mult(a1s,2)
    a2s = gf_mult(a2s,4)

print(f"{a0s}, {a1s}, {a2s}")