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

x = 2
x2 = gf_mult(x,x)
x4 = gf_mult(x2,x2)
x8 = gf_mult(x4,x4)
x16 = gf_mult(x8,x8) 
x32 = gf_mult(x16,x16) 
x64 = gf_mult(x32,x32) 
x128 = gf_mult(x64,x64)

x6 = gf_mult(x2, x4)
x14 = gf_mult(x6, x8)
x30 = gf_mult(x14, x16)
x62 = gf_mult(x30, x32)
x126= gf_mult(x62, x64)
x_inv = gf_mult(x126, x128)

print(f"{x}, inv1: {x_inv}, inv2 :{gf_inv(x)}")

print(f"x2: {x2}")
print(f"x4: {x4}")
print(f"x8: {x8}")
print(f"x16: {x16}")
print(f"x32: {x32}")
print(f"x64: {x64}")
print(f"x128: {x128}")
print(f"x6: {x6}")
print(f"x14: {x14}")
print(f"x30: {x30}")
print(f"x62: {x62}")
print(f"x126: {x126}")