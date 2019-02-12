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

with open('/home/omarcartera/Desktop/repos/GP_Streamer/live_server/Z001.txt', 'r') as f:
	for line in f:
		line += '\n'

		s.send(line)
		time.sleep(0.1)

s.close()