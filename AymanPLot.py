import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA, PCA
import csv
from scipy import signal

import time


#
# dataset=sio.loadmat('signal.mat')
# sig=dataset['signal']
# samp=sig[20,:,:]
#
sig = []

with open('/home/omarcartera/Desktop/ideeha.txt', 'r') as f:
    for line in f:

        sig.append(float(line.split('a')[0]))

print(len(sig))

print sig[0:3]

fs = 250.0  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
Q = 30.0  # Quality factor
w0 = f0/(fs/2)  # Normalized Frequency
b, a = signal.iirnotch(w0, Q)
# # #
# #
nyq=0.5*fs
low_cut=4/nyq
high_cut=40/nyq
b1, a1=signal.butter(2,[low_cut,high_cut],'bandpass')

N = 250
random_x = np.linspace(0,N,N)
# random_x = np.linspace(0,125,125)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.set_ylim([np.amin(sig), np.amax(sig)])
ax.set_title('All channels')
ax.set_xlabel('Time')
ax.set_ylabel('voltage')
# line1,  = ax.plot(abs(np.fft.fft(sig[0:N]))[0:125])
line1,  = ax.plot(signal.filtfilt(b1,a1,signal.filtfilt(b,a,sig[0:N])))

ix = 0

while ix  < len(sig):
    start_time = time.time()

    # line1.set_ydata(abs(np.fft.fft(sig[ix:ix+N]))[0:125])
    line1.set_ydata(signal.filtfilt(b1,a1,signal.filtfilt(b,a,sig[ix:ix+N])))
    fig.canvas.draw()
    fig.canvas.flush_events()
    ix += 1

    print("--- %s seconds ---" % (time.time() - start_time))
