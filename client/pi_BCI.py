import argparse
import os
import string
import atexit
import threading
import logging
import sys
import time, timeit
import Queue
import open_bci_v3 as bci
import scipy.io as sio
import atexit
import numpy as np


import socket

import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA, PCA
from scipy import signal

sig = []

TCP_IP = '127.0.0.1'
TCP_PORT = 4564
BUFFER_SIZE = 1024

connected = False


while not connected:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))

		connected = True

	except:
		print 'Waiting for a server...'
		time.sleep(2)


board = bci.OpenBCIBoard(port="/dev/ttyUSB0", scaled_output=True)

board.streaming = False
if not board.streaming:
	board.ser.write(b'b')
	board.streaming = True


ch = [0, 0, 0, 0, 0, 0, 0, 0]
line = ''
filename = 'test.txt'

fs   = 250.0  # Sample frequency (Hz)
f0   = 50.0  # Frequency to be removed from signal (Hz)
Q    = 30.0  # Quality factor
w0   = f0/(fs/2)  # Normalized Frequency
b, a = signal.iirnotch(w0, Q)


nyq  = 0.5*fs
low_cut = 4/nyq
high_cut = 40/nyq
b1, a1 = signal.butter(2,[low_cut,high_cut],'bandpass')

N = 50
random_x = np.linspace(0,N,N)

ix = 0

# random_x = np.linspace(0,125,125)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

# ax.set_ylim([np.amin(sig), np.amax(sig)])
ax.set_title('All channels')
ax.set_xlabel('Time')
ax.set_ylabel('voltage')
# line1,  = ax.plot(abs(np.fft.fft(sig[0:N]))[0:125])


with open(filename, 'w') as file:
	with open('filtered.txt', 'w') as filtered:

		print ("start streaming")
		start_time = time.time()

		for j in range (2500):
			samp=board._read_serial_binary()

			ch[0] = samp.channel_data[0]
			ch[1] = samp.channel_data[1]
			ch[2] = samp.channel_data[2]
			ch[3] = samp.channel_data[3]
			ch[4] = samp.channel_data[4]
			ch[5] = samp.channel_data[5]
			ch[6] = samp.channel_data[6]
			ch[7] = samp.channel_data[7]

			sig.append(float(ch[0]))

			for i in range(7):
				line += str(ch[i]) + 'a'

			line += str(ch[7])
			line += '\n'

			file.write(line)
			s.send(line)
			time.sleep(0.1)

			if len(sig) > N:
				line1,  = ax.plot(signal.filtfilt(b1,a1,signal.filtfilt(b,a,sig[0:N])))


				plt.ion()

				line1.set_ydata(signal.filtfilt(b1,a1,signal.filtfilt(b,a,sig[ix:ix+N])))
				fig.canvas.draw()
				fig.canvas.flush_events()

				ix += 1

			line = ''

			print j