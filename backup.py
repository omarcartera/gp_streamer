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

# import design.py for GUI things
import design
import sys

# to open files and sleep()
import os
import time

#socket things
import socket
from thread import *

# to play sound files
import pygame

# wireless part
from wireless import Wireless

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

'''
import platform

if(platform.system() == 'Linux'):
	from gi.repository import Notify, GdkPixbuf

if(platform.system() == 'Windows'):
	from win10toast import ToastNotifier
'''

# progress bar GUI thread
class graph_thread(QtCore.QThread):
	def __init__(self):
		super(graph_thread, self).__init__()

	# call the function that updates the bar from the secondary thread
	def run(self):
		while 1:
			try:
				self.emit(SIGNAL('draw()'))
				QThread.msleep(500)

			except(TypeError):
				pass


# main GUI class
class mainApp(QtGui.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		super(mainApp, self).__init__()
		self.setupUi(self)

		#style.use('grayscale')
		#style.use('fivethirtyeight')
		style.use('classic')

		# GUI thread things
		self.graph_thread = graph_thread()
		self.connect(self.graph_thread, SIGNAL('draw()'), self.draw)
		
		self.a = []
		self.b = []

		self.counter = 0

		self.x_min = 0
		self.x_max = 20

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

		# connecting the GUI objects to their methods
		self.lndt_host.setFocus(True)

		try:
			wireless = Wireless()

			if (wireless.current() == 'RUN'):
				self.lndt_host.setText('192.168.1.')

			else:
				self.lndt_host.setText('172.28.130.')

		except:
			self.lndt_host.setText('172.28.130.')


		self.btn_server.clicked.connect(self.server_conn)
		self.btn_client.clicked.connect(self.client_conn)

		# press enter to connect as a client to the given server
		self.lndt_host.returnPressed.connect(self.client_conn)

		# setting the chat socket connection parameters
		self.host = ''
		self.port = 5557

		# establishing a TCP connection for the chat server
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# this line allows re-using the same socket even if it was closed improperly
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		## self.graph_thread.start()

'''
	# sending messages to the chat room
	def send_chat(self):
		if (self.lndt_msg.text() == ''):
			# set the chat box borders to red if sending blank
			self.lndt_msg.setStyleSheet("border: 1px solid red")

		else:
			# set the chat box borders to grey if sending anything other than blank
			self.lndt_msg.setStyleSheet("border: 1px solid grey")

			# try sending to every client in the room
			# clients only send to the server,
			# while the server sends to all clients
			for i in range(len(self.conn_list)):
				# every packet I send is in the form (my_computer_name`my_msg)
				# getfqdn() gets my computer name
				self.conn_list[i].send(socket.getfqdn() + '`' + str(self.lndt_msg.text()))
			
			# setting Your message clolr to RED
			self.txt_chat.setTextColor(QColor(200, 0, 0))
			self.txt_chat.append('You: ' + self.lndt_msg.text())

			# scroll down the chat box to the end after every appending
			self.txt_chat.moveCursor(QtGui.QTextCursor.End)

			# setting the color back to BLACK
			self.txt_chat.setTextColor(QColor(50, 50, 50))

			# send the 'I finished typing' signal
			self.conn_list[0].send(socket.getfqdn() + '`' + 'typn-')

			# clear the message box
			self.lndt_msg.clear()
'''


	# when this host is the server
	def server_conn(self):
		# raising the server flag
		self.isServer = True

		self.lndt_msg.setFocus(True)
		self.lndt_host.clear()

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
			print('Waiting for connection...')

			try:
				# accept the incoming clients connection request
				self.conn, self.addr = self.s.accept()

				# get the IP of this client
				self.addr = self.addr[0]

				# append the new client's IP and connection to their lists
				self.addr_list.append(self.addr)
				self.conn_list.append(self.conn)

				self.txt_online.append(self.addr)


				print('Connected to:' + self.addr)

				print self.addr_list
				print self.conn_list

				# if this is the first client
				if(self.i == 0):
					# run the first client thread
					start_new_thread(self.threaded_client_1, (self.conn_list[0],))

				# if this is the second client
				elif(self.i == 1):
					# run another thread for the second client
					start_new_thread(self.threaded_client_2, (self.conn_list[1],))

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
			print 'data_1: ' + self.data[0]

			if not self.data[0]:
				break
			
			# extract the sender name and message content from the received packet
			# the name and the content are separated by '`'
			self.sender = self.data[0].partition('`')[0]
			self.data[0] = self.data[0][self.data[0].index('`') + 1:]

			if (self.sender != socket.getfqdn()):
				# el mafrood a-broadcast el typing signals dee brdo
				# if it is sending a 'is typing' signal
				if (self.data[0] == 'typn+'):
					self.lbl_typing.setText(self.sender + ' is typing...')
					#self.data[0] = ' '

				# if it is sending 'stopped typing' signal
				elif (self.data[0] == ('typn-' + self.sender +'`typn+')):
					self.lbl_typing.clear()
					#self.data[0] = ' '

				elif (self.data[0].startswith('typn')):
					self.lbl_typing.clear()
					#self.data[0] = ' '

				elif (self.data[0] == ('typn-')):
					self.lbl_typing.clear()
					#self.data[0] = ' '

				# if it is sending a message 3ady ya3ny
				else:
					try:
						if(platform.system() == 'Linux'):
							self.bubble.update(self.sender, self.data[0])
							self.bubble.show()

						if(platform.system() == 'Windows'):
							self.balloon.show_toast(self.sender, self.data[0], duration = 6, threaded = True)

						# play the notification sound
						pygame.mixer.Sound('notification.wav').play()

						# add the received data to the chat room
						self.txt_chat.append(str(self.sender) +': ' + self.data[0])
						self.txt_chat.moveCursor(QtGui.QTextCursor.End)


					except AttributeError as e:
						self.txt_chat.append(str(self.host) +': ' + self.data[0])
						self.txt_chat.moveCursor(QtGui.QTextCursor.End)

				# if I'm the server --> broadcast to other clients
				if (self.isServer):
					print 'broadcaster_1'
					self.broadcast()


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


	def draw(self):
		self.clearLayout(self.streaming_plot)
		self.fig2 = Figure()
		self.fig2.patch.set_facecolor('white')
		self.ax1f2 = self.fig2.add_subplot(111)
		
		if(len(self.a) == 20):
			self.a.pop(0)
			self.b.pop(0)
			self.x_min += 1
			self.x_max += 1

		self.a.append(self.counter)
		self.b.append(self.dial.value())

		#self.ax1f2.set_xlim(self.counter, self.counter+20)
		self.ax1f2.set_ylim(0, 15)
		self.ax1f2.set_xlim(self.x_min, self.x_max)

		self.ax1f2.plot(self.a, self.b)

		print len(self.a), len(self.b)

		self.canvas = FigureCanvas(self.fig2)
		self.streaming_plot.addWidget(self.canvas)
		self.canvas.draw()

		self.counter += 1



def main():
	App = QtGui.QApplication(sys.argv)
	form = mainApp()
	form.show()
	App.exec_()
	

if __name__ == '__main__':
	main()
