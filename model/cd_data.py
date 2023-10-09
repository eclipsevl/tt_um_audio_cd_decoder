from rs_enc_dec_32_28 import decode

f1 = open("./sdram_dump_data")
f2 = open("./sdram_dump_misc")

data = f1.readlines()
misc = f2.readlines()

frames = []
frame = [0] * 33

curr_index = 0

frm_cnt = 7350*10

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

        if((int(misc[curr_index])&0x3f) != j):
            print(f"sync error! {int(misc[curr_index])} != {j}")
            curr_index = curr_index + 1
            break

        curr_index = curr_index + 1
    
    frames.append(frame.copy())
    #print(frame)


#construct C1 frames
#print("C1 Frames:")
frame_c1 = [0] * 32
frames_c1 = []
frame_c2 = [0] * 32
frames_c2 = []

def inv_8bit(a):
    return (~a & 0xFF)


for i in range(1, frm_cnt-1):
    for j in range(16):
        frame_c1[j * 2] = frames[i][j * 2 + 1]
        frame_c1[j * 2 + 1] = frames[i - 1][j * 2 + 1 + 1]

    #print(frame_c1)

    frame_c1[12] = inv_8bit(frame_c1[12])
    frame_c1[13] = inv_8bit(frame_c1[13])
    frame_c1[14] = inv_8bit(frame_c1[14])
    frame_c1[15] = inv_8bit(frame_c1[15])

    frame_c1[28] = inv_8bit(frame_c1[28])
    frame_c1[29] = inv_8bit(frame_c1[29])
    frame_c1[30] = inv_8bit(frame_c1[30])
    frame_c1[31] = inv_8bit(frame_c1[31])


    frames_c1.append(frame_c1.copy())



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

def calc_parity_c1(_c1_frame):
    s0 = 0
    s1 = 0
    a1 = 1
    s2 = 0
    a2 = 1

    s3 = 0
    a3 = 1

    #frames_c1[j] = [254, 182, 6, 40, 6, 116, 0, 164, 2, 51, 0, 104, 203, 64, 173, 146, 11, 28, 145, 162, 6, 54, 5, 0, 15, 28, 5, 169, 67, 188, 98, 110]
    for i in range(32):
        s0 = gf_add(_c1_frame[i], s0)
        s1 = gf_add(gf_mult(_c1_frame[31-i],a1), s1)
        a1 = gf_mult(a1, 2)

        s2 = gf_add(gf_mult(_c1_frame[31-i],a2), s2)
        a2 = gf_mult(a2, 4)

        s3 = gf_add(gf_mult(_c1_frame[31-i],a3), s3)
        a3 = gf_mult(a3, 4)

    return [s0,s1,s2,s3]

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

c1_correct = 0
c1_corrected = 0
c2_correct = 0
c2_corrected = 0
#check parity
for j in range(frm_cnt-2):
    #print(frames_c1[j])

    s0,s1,s2,s3 = calc_parity_c1(frames_c1[j])

    #print(f"{s0},{s1},{s2},{s2}")
    if(s0 == 0 and s1 == 0 and s2 == 0 and s3 == 0):
        c1_correct = c1_correct+1
    else:
        frames_c1[j] = decode(frames_c1[j])
        s0,s1,s2,s3 = calc_parity_c1(frames_c1[j])

        if(s0 == 0 and s1 == 0 and s2 == 0 and s3 == 0):
            c1_corrected = c1_corrected+1

        

print(f"Summary: correct frames: {c1_correct}, corrected frames: {c1_corrected}, total: {c1_correct+c1_corrected}/{frm_cnt-2}")

for i in range(4 * 27, frm_cnt-2):
    for j in range(28):
        frame_c2[j] = frames_c1[i - (27-j)*4][j];

    frames_c2.append(frame_c2.copy())

for j in range(len(frames_c2)):
    #print(frames_c1[j])

    s0,s1,s2,s3 = calc_parity_c2(frames_c2[j])

    #print(f"{s0},{s1},{s2},{s2}")
    if(s0 == 0 and s1 == 0 and s2 == 0 and s3 == 0):
        c2_correct = c2_correct+1
        #print(f"C2: {frames_c2[j]}")
    else:
        frames_c2[j] = decode(frames_c2[j])
        s0,s1,s2,s3 = calc_parity_c2(frames_c2[j])

        if(s0 == 0 and s1 == 0 and s2 == 0 and s3 == 0):
            c2_corrected = c2_corrected+1

print(f"Summary: correct frames: {c2_correct}, corrected frames: {c2_corrected}, total: {c2_correct+c2_corrected}/{frm_cnt-2}")


# assemble samples

fp1 = open("left", "w");
fp2 = open("right", "w");

for i in range(2,frm_cnt-150):
    l0 = (frames_c2[i][0] << 8) + frames_c2[i][1]
    r0 = (frames_c2[i][6] << 8) + frames_c2[i][7]

    l1 = (frames_c2[i - 2][16] << 8) + frames_c2[i - 2][17]
    r1 = (frames_c2[i - 2][22] << 8) + frames_c2[i - 2][23]

    l2 = (frames_c2[i][2] << 8) + frames_c2[i][3]
    r2 = (frames_c2[i][8] << 8) + frames_c2[i][9]

    l3 = (frames_c2[i - 2][18] << 8) + frames_c2[i - 2][19]
    r3 = (frames_c2[i - 2][24] << 8) + frames_c2[i - 2][25]

    l4 = (frames_c2[i][4] << 8) + frames_c2[i][5]
    r4 = (frames_c2[i][10] << 8) + frames_c2[i][11]

    l5 = (frames_c2[i - 2][20] << 8) + frames_c2[i - 2][21]
    r5 = (frames_c2[i - 2][26] << 8) + frames_c2[i - 2][27]
    
    fp1.write(f"{l0}\n{l1}\n{l2}\n{l3}\n{l4}\n{l5}\n")
    fp2.write(f"{r0}\n{r1}\n{r2}\n{r3}\n{r4}\n{r5}\n")

# No C1, No C2 correction
#Summary: correct frames: 6859, corrected frames: 0, total: 6859/73498
#Summary: correct frames: 1681, corrected frames: 0, total: 1681/73498

# C1 correction, no C2 correction
#Summary: correct frames: 6859, corrected frames: 27638, total: 34497/73498
#Summary: correct frames: 3289, corrected frames: 0, total: 3289/73498

# C1, C2 correction
#Summary: correct frames: 6859, corrected frames: 27638, total: 34497/73498
#Summary: correct frames: 3289, corrected frames: 6946, total: 10235/73498