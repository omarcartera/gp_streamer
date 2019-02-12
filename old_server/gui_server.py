# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_server.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(695, 455)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.streamer = QtGui.QWidget(self.centralwidget)
        self.streamer.setGeometry(QtCore.QRect(10, 59, 671, 351))
        self.streamer.setObjectName(_fromUtf8("streamer"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 161, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.lbl_error = QtGui.QLabel(self.centralwidget)
        self.lbl_error.setGeometry(QtCore.QRect(240, 30, 221, 17))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(204, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lbl_error.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lbl_error.setFont(font)
        self.lbl_error.setText(_fromUtf8(""))
        self.lbl_error.setTextFormat(QtCore.Qt.RichText)
        self.lbl_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_error.setObjectName(_fromUtf8("lbl_error"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 695, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Added by the magnificent me to allow plotting
        self.streaming_plot = QtGui.QVBoxLayout(self.streamer)
        self.streaming_plot.setObjectName(_fromUtf8("streamLayout"))
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ModMen® Production | EEG Server", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "1", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "2", None))

