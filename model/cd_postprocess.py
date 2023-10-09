import matplotlib.pyplot as plt
import numpy as np
import math   
from scipy import signal
import scipy

samples_file = open("./left", "r")
samples_left = samples_file.readlines()

samples_file = open("./right", "r")
samples_right = samples_file.readlines()

samples_left_int = []
samples_right_int = []



for sample in samples_left:
    samples_left_int.append(int(sample))
    
for sample in samples_right:
    samples_right_int.append(int(sample))
  
scipy.io.wavfile.write("left.wav", 44100, np.array(samples_left_int).astype(np.int16))
scipy.io.wavfile.write("right.wav", 44100, np.array(samples_right_int).astype(np.int16))  

proc_length = len(samples_left_int)-3
fs = 44100
dt = 1/fs

t_end = dt*(proc_length-1)
t = np.arange(0.0, t_end, dt)

   
plt.plot(t, np.array(samples_left_int).astype(np.int16)[0:proc_length], 'ro--')
plt.plot(t, np.array(samples_right_int).astype(np.int16)[0:proc_length], 'bo--')
plt.show()
plt.ylabel('Samples')