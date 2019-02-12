#!/usr/bin/env python

#/******************************
# *     Author: Omar Gamal     *
# *   c.omargamal@gmail.com    *
# *                            *
# *    Language: Python2.7     *
# *                            *
# *         15/1/2018          *
# *                            *
# *      TCP Multi-Client      *
# *      Chat Application      *
# ******************************/

'''
#####################################################################################
        #Added by the magnificent me to allow plotting
        self.streaming_plot = QtGui.QVBoxLayout(self.streamer)
        self.streaming_plot.setObjectName(_fromUtf8("streamLayout"))
######################################################################################
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType

# import gui_server.py for GUI things
import gui_server
import sys

# to open files and sleep()
import os
import time

#socket things
import socket
from thread import *

# to play sound files
import pygame

#################################
import numpy as np
#from numpy import interp

from matplotlib import style

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

import pylab
#################################


# progress bar GUI thread
class graph_thread(QtCore.QThread):
	def __init__(self):
		super(graph_thread, self).__init__()

	# call the function that updates the bar from the secondary thread
	def run(self):
		while 1:
			try:
				self.emit(SIGNAL('add_value_1()'))
				self.emit(SIGNAL('add_value_2()'))
				self.emit(SIGNAL('draw()'))
				QThread.msleep(500)

			except(TypeError):
				pass


# main GUI class
class mainApp(QtGui.QMainWindow, gui_server.Ui_MainWindow):
	def __init__(self):
		super(mainApp, self).__init__()
		self.setupUi(self)

		style.use('grayscale')
		#style.use('fivethirtyeight')
		#style.use('classic')

		# GUI thread things
		self.graph_thread = graph_thread()
		self.connect(self.graph_thread, SIGNAL('draw()'), self.draw)
		self.connect(self.graph_thread, SIGNAL('add_value_1()'), self.add_value_1)
		self.connect(self.graph_thread, SIGNAL('add_value_2()'), self.add_value_2)

		self.a = []
		self.b = []

		self.c = []
		self.d = []

		self.counter_1 = 0
		self.counter_2 = 0


		self.x_min_1 = 0
		self.x_max_1 = 20

		self.x_min_2 = 0
		self.x_max_2 = 20

		self.thing = 5

		self.error_msg = ''

		# starting pygame
		pygame.init()

		'''
		# initialize notification object
		if(platform.system() == 'Linux'):
			Notify.init('indistinct chatter')
			self.bubble = Notify.Notification.new('!', '?')
			image = GdkPixbuf.Pixbuf.new_from_file('')
			self.bubble.set_icon_from_pixbuf(image)

		if(platform.system() == 'Windows'):
			self.balloon = ToastNotifier()
		'''

		# flag to tell if this host is a server
		self.isServer = False

		# data received from clients
		self.data = ['.', '.']

		# ip and connection info about chat clients
		self.addr_list = []
		self.conn_list = []

		# clients counter: chat client i .. media client j
		self.i = 0
		self.j = 0


		#self.btn_start.clicked.connect(self.server_conn)

		# setting the chat socket connection parameters
		self.host = ''
		self.port = 5557

		# establishing a TCP connection for the chat server
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# this line allows re-using the same socket even if it was closed improperly
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_conn()

	# when this host is the server
	def server_conn(self):
		# raising the server flag
		self.isServer = True

		# starting a thread to keep listening to any connecting client
		# threaded to work in the background without interrupting the main thread
		start_new_thread(self.threaded_server, ())

		self.graph_thread.start()


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

				print self.addr_list
				print self.conn_list

				# if this is the first client
				if(self.i == 0):
					# run the first client thread
					start_new_thread(self.threaded_client_1, (self.conn_list[0],))

				# if this is the second client
				elif(self.i == 1):
					pass
					# run another thread for the second client
					#start_new_thread(self.threaded_client_2, (self.conn_list[1],))

				# increment the number of connecting clients
				self.i += 1


			except KeyboardInterrupt:
				if self.conn:
					self.conn.close()



	# if this host is a client
	def client_conn(self):
		if (self.lndt_host.text() == ''):
			# setting host ip box borders to red if blank
			self.lndt_host.setStyleSheet("border: 1px solid red")

		else:
			try:
				# setting host ip box borders to grey if not blank
				self.lndt_host.setStyleSheet("border: 1px solid grey")

				# give it the server host IP, connect to it
				self.host = str(self.lndt_host.text())
				self.s.connect((self.host, self.port))
				self.conn = self.s
				self.conn_list.append(self.conn)

				# run a client thread to receive chat messages from the server
				start_new_thread(self.threaded_client_1, (self.conn,))

				# give it the server host IP, connect to it 'media things'
				self.media_host = str(self.lndt_host.text())
				self.media_s.connect((self.media_host, self.media_port))
				self.media_conn = self.media_s
				self.media_conn_list.append(self.media_conn)

				# run a client thread to receive media from the server
				start_new_thread(self.media_client_1, ())
				self.lbl_error.clear()
				self.lndt_msg.setFocus(True)

			except socket.error:
				self.lbl_error.setText("No server at this IP!")




	# a thread that keeps polling any incoming data from a client/sender
	def threaded_client_1(self,client_conn):
		while True:
			# wait to receive data from client 1
			self.data[0] = self.conn_list[0].recv(2048)
			print 'data_0: ' + self.data[0]

			if not self.data[0]:
				break
			

		# close the connection with that client
		self.conn_list[0].close()




	## clearing any given plot. Courtsey: Mahmoud Fathy
	def clearLayout(self, layout):
		for i in reversed(range(layout.count())):
			item = layout.itemAt(i)

			if isinstance(item, QtGui.QWidgetItem):
				#print "widget" + str(item)
				item.widget().close()
				# or
				# item.widget().setParent(None)
			elif isinstance(item, QtGui.QSpacerItem):
				k=0
				#print "spacer " + str(item)
				# no need to do extra stuff
			else:
				#print "layout " + str(item)
				self.clearLayout(item.layout())

			# remove the item from layout
			layout.removeItem(item)


	def add_value_1(self):
		if(len(self.b) == 20):
			self.a.pop(0)
			self.b.pop(0)
			self.x_min_1 += 1
			self.x_max_1 += 1

		try:
			self.b.append(int(self.data[0]))
			self.error_msg = ''

		except (ValueError):
			self.b.append(0)
			self.error_msg = 'Client Disconnected'


		self.a.append(self.counter_1)

		print len(self.a), len(self.b)

		self.counter_1 += 1




	def add_value_2(self):
		if(len(self.d) == 20):
			self.c.pop(0)
			self.d.pop(0)
			self.x_min_2 += 1
			self.x_max_2 += 1

		self.d.append(self.thing)
		self.c.append(self.counter_2)

		self.counter_2 += 1

		self.thing *= -1



	def draw(self):
		self.clearLayout(self.streaming_plot)
		
		self.fig2 = Figure()
		self.fig2.patch.set_facecolor('white')
		self.ax1f2 = self.fig2.add_subplot(111)

		#self.ax1f2.set_xlim(self.counter, self.counter+20)
		self.ax1f2.set_ylim(-15, 15)

		if(self.comboBox.currentText() == '1'):
			self.ax1f2.plot(self.a, self.b)
			self.ax1f2.set_xlim(self.x_min_1, self.x_max_1)
			self.lbl_error.setText(self.error_msg)

		if(self.comboBox.currentText() == '2'):
			self.ax1f2.plot(self.c, self.d)
			self.ax1f2.set_xlim(self.x_min_2, self.x_max_2)
			self.lbl_error.clear()


		self.canvas = FigureCanvas(self.fig2)
		self.streaming_plot.addWidget(self.canvas)
		self.canvas.draw()





def main():
	App = QtGui.QApplication(sys.argv)
	form = mainApp()
	form.show()
	App.exec_()
	

if __name__ == '__main__':
	main()
