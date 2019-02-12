from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import QThread, SIGNAL

from scipy import signal
import scipy.io as sio

import pyqtgraph

import ui_main

import sys
import os
import time

import numpy as np
import pylab

import socket
from thread import *
#####################################

class plotting_thread(QtCore.QThread):
	def __init__(self):
		super(plotting_thread, self).__init__()

	def run(self):
		self.emit(SIGNAL('update()'))

		while(1):
			try:
				self.emit(SIGNAL('add_value()'))

				QThread.msleep(10)

			except(TypeError):
				pass


class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
	def __init__(self, parent=None):
		
		pyqtgraph.setConfigOption('background', 'w') #before loading widget

		super(ExampleApp, self).__init__(parent)
		self.setupUi(self)

		self.plotting_thread = plotting_thread()
		self.connect(self.plotting_thread, SIGNAL('update()'), self.update)
		self.connect(self.plotting_thread, SIGNAL('add_value()'), self.add_value)

		self.grPlot.plotItem.showGrid(True, True, 1)

		self.samples = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
		self.time    = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

		self.counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		self.color = [(0,0,0), (255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
		self.error_msg = 'Disconnected'


		# flag to tell if this host is a server
		self.isServer = False

		# data received from clients
		self.data = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']

		# ip and connection info about chat clients
		self.addr_list = []
		self.conn_list = []

		# clients counter: chat client i .. media client j
		self.i = 0

		# setting the chat socket connection parameters
		self.host = ''
		self.port = 4564

		# establishing a TCP connection for the chat server
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# this line allows re-using the same socket even if it was closed improperly
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		self.lbl_error.setStyleSheet('color: red')
		try:
			err = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0] + ':' + str(self.port)
			self.lbl_ip.setText(err)

		except:
			self.lbl_ip.setText('No WiFi')
		
		self.server_conn()

		self.alarm = 0
		self.which = 0

		self.temp_data = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]


	def update(self):
		if self.alarm == '1':
			self.pen = pyqtgraph.mkPen(color = (255, 0, 0), width = 10)
		
		else:
			self.pen = pyqtgraph.mkPen(color = self.color[self.ch_combo.currentIndex()], width = 5)
		
		try:
			# self.grPlot.setYRange(2 * np.min(self.samples[(self.pt_combo.currentIndex() * 8) + self.ch_combo.currentIndex()]), 2 * np.max(self.samples[(self.pt_combo.currentIndex() * 8) + self.ch_combo.currentIndex()]))
			self.grPlot.setYRange(-1000, 1000)

		except:
			self.grPlot.setYRange(-10000, 10000)

		self.lbl_error.setText(str(self.error_msg))

		if self.error_msg == 'Connected':
			self.lbl_error.setStyleSheet('color: green')

		else:
			self.lbl_error.setStyleSheet('color: red')

		try:
			self.grPlot.plot(self.time[(self.pt_combo.currentIndex() * 8) + self.ch_combo.currentIndex()], self.samples[(self.pt_combo.currentIndex() * 8) + self.ch_combo.currentIndex()], pen = self.pen, clear = True)

		except Exception as e:
			pass

		QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat




	# when this host is the server
	def server_conn(self):
		# raising the server flag
		self.isServer = True

		# starting a thread to keep listening to any connecting client
		# threaded to work in the background without interrupting the main thread
		start_new_thread(self.threaded_server, ())

		self.plotting_thread.start()



	# server thread
	def threaded_server(self):
		while True:
			try:
				# creating a chat server at the given port
				self.s.bind((self.host, self.port))

			except socket.error:
				pass


			self.s.listen(5)
			print('Waiting for connection...\n')

			try:
				# accept the incoming clients connection request
				self.conn, self.addr = self.s.accept()

				# get the IP of this client
				self.addr = self.addr[0]

				# append the new client's IP and connection to their lists
				self.addr_list.append(self.addr)
				self.conn_list.append(self.conn)

				print('Connected to:' + self.addr)


				start_new_thread(self.threaded_client_1, (self.conn_list[self.which], self.which,))

				self.which += 1


				# increment the number of connecting clients
				self.i += 1


			except KeyboardInterrupt:
				if self.conn:
					self.conn.close()



	# a thread that keeps polling any incoming data from a client/sender
	def threaded_client_1(self, conn, which):
		while True:
			if which == 0:
				# wait to receive data from client 1
				received_data = conn.recv(2048).split('\n')
				tit = received_data[0] + 'a' + received_data[0] + '\n'

				received_data = received_data[0].split('a')

				if received_data == ['']:
					pass

				else:				
					for k in range(8):
						self.data[(which * 8) + k] = float(received_data[k])


					self.alarm = received_data[0]


				if(np.random.randint(0, 500) == 7):
					tit = 'b' + tit
					print 'ALARM!!'

				try:
					self.error_msg = 'Connected'

					self.conn_list[-1].send(tit)
					time.sleep(0.05)

				except:
					self.error_msg = 'Disconnected'

			else:
				pass

		# close the connection with that client
		conn.close()



	def add_value(self):
		ch_num = self.ch_combo.currentIndex()
		pt_num = self.pt_combo.currentIndex()

		if(len(self.time[(pt_num * 8) + ch_num]) == 250):
			self.samples[(pt_num * 8) + ch_num] = self.ideeha((self.temp_data[(pt_num * 8) + ch_num]))

			self.temp_data[(pt_num * 8) + ch_num].pop(0)
			self.time[(pt_num * 8) + ch_num].pop(0)

		try:
			self.temp_data[(pt_num * 8) + ch_num].append(int(self.data[(pt_num * 8) + ch_num]))
			try:
				if(len(self.time[(pt_num * 8) + ch_num]) < 500):
					self.samples[(pt_num * 8) + ch_num].append(int(self.data[(pt_num * 8) + ch_num]))

			except:
				pass

		except (ValueError):
			self.temp_data[(pt_num * 8) + ch_num].append(0)

			try:
				if(len(self.time[(pt_num * 8) + ch_num]) < 500):
					self.samples[(pt_num * 8) + ch_num].append(0)
			except:
				pass

		self.time[(pt_num * 8) + ch_num].append(self.counter[(pt_num * 8) + ch_num])

		self.counter[(pt_num * 8) + ch_num] += 1

		print len(self.samples[(pt_num * 8) + ch_num])


	def ideeha(self, data):
		fs   = 250.0  # Sample frequency (Hz)
		f0   = 50.0  # Frequency to be removed from signal (Hz)
		Q    = 30.0  # Quality factor
		w0   = f0/(fs/2)  # Normalized Frequency
		b, a = signal.iirnotch(w0, Q)


		nyq  = 0.5*fs
		low_cut = 4/nyq
		high_cut = 40/nyq
		b1, a1 = signal.butter(2,[low_cut,high_cut],'bandpass')
		data = signal.filtfilt(b1,a1,signal.filtfilt(b,a,data))

		return data



if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	form.update() #start with something
	app.exec_()
	print("DONE")
	sys.exit()
	#form._7amada() #here you can call any function :O