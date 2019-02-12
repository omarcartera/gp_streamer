#!/usr/bin/env python

import time
import socket
import numpy as np


ch = [0, 0, 0, 0, 0, 0, 0, 0]

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


while 1:
	for i in range(1, 9):
		ch[i-1] = str(np.random.randint(0, 1000*i*i))

	
	seizure = str(np.random.randint(0, 10))
	msg = ch[0] + 'a' + ch[1] + 'a' + ch[2] + 'a' + ch[3] + 'a' + ch[4] + 'a' + ch[5] + 'a' + ch[6] + 'a' + ch[7] + '\n'

	s.send(msg)
	time.sleep(0.05)

s.close()