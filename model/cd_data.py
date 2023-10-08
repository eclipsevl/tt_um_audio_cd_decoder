f1 = open("./sdram_dump_data")
f2 = open("./sdram_dump_misc")

data = f1.readlines()
misc = f2.readlines()

frames = []
frame = [0] * 33

curr_index = 0

frm_cnt = 16

#find start
for i in range(256):
    if int(misc[i]) == 0:
        curr_index = i
        break

#load 16 frames
print("Frames:")
for i in range(frm_cnt):
    for j in range(33):
        frame[j] = int(data[curr_index])        

        if(int(misc[curr_index]) != j):
            print(f"sync error! {int(misc[curr_index])} != {j}")

        curr_index = curr_index + 1
    
    frames.append(frame.copy())
    print(frame)


#construct C1 frames
print("C1 Frames:")
frame_c1 = [0] * 32
frames_c1 = []

def inv_8bit(a):
    return (~a & 0xFF)


for i in range(1, frm_cnt-1):
    for j in range(16):
        frame_c1[j * 2] = frames[i][j * 2 + 1]
        frame_c1[j * 2 + 1] = frames[i - 1][j * 2 + 1 + 1]

    print(frame_c1)

    frame_c1[12] = inv_8bit(frame_c1[12])
    frame_c1[13] = inv_8bit(frame_c1[13])
    frame_c1[14] = inv_8bit(frame_c1[14])
    frame_c1[15] = inv_8bit(frame_c1[15])

    frame_c1[28] = inv_8bit(frame_c1[28])
    frame_c1[29] = inv_8bit(frame_c1[29])
    frame_c1[30] = inv_8bit(frame_c1[30])
    frame_c1[31] = inv_8bit(frame_c1[31])


    frames_c1.append(frame_c1.copy())


def gf_add(a, b):
    return a ^ b
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

#check parity
for j in range(frm_cnt-2):
    #print(frames_c1[j])


    s0 = 0
    s1 = 0
    a1 = 1
    s2 = 0
    a2 = 1

    s3 = 0
    a3 = 1

    #frames_c1[j] = [254, 182, 6, 40, 6, 116, 0, 164, 2, 51, 0, 104, 203, 64, 173, 146, 11, 28, 145, 162, 6, 54, 5, 0, 15, 28, 5, 169, 67, 188, 98, 110]
    for i in range(32):
        s0 = gf_add(frames_c1[j][i], s0)
        s1 = gf_add(gf_mult(frames_c1[j][31-i],a1), s1)
        a1 = gf_mult(a1, 2)

        s2 = gf_add(gf_mult(frames_c1[j][31-i],a2), s2)
        a2 = gf_mult(a2, 4)

        s3 = gf_add(gf_mult(frames_c1[j][31-i],a3), s3)
        a3 = gf_mult(a3, 4)
        

    print(f"{s0},{s1},{s2},{s2}")