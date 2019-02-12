# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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
        MainWindow.resize(812, 650)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line_6 = QtGui.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.verticalLayout.addWidget(self.line_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.line_7 = QtGui.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtGui.QFrame.VLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.horizontalLayout.addWidget(self.line_7)
        self.pt_combo = QtGui.QComboBox(self.centralwidget)
        self.pt_combo.setObjectName(_fromUtf8("pt_combo"))
        self.pt_combo.addItem(_fromUtf8(""))
        self.pt_combo.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.pt_combo)
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout.addWidget(self.line_3)
        self.ch_combo = QtGui.QComboBox(self.centralwidget)
        self.ch_combo.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.ch_combo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ch_combo.setObjectName(_fromUtf8("ch_combo"))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.ch_combo.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.ch_combo)
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.horizontalLayout.addWidget(self.line_4)
        self.lndt_filename = QtGui.QLineEdit(self.centralwidget)
        self.lndt_filename.setMinimumSize(QtCore.QSize(50, 27))
        self.lndt_filename.setObjectName(_fromUtf8("lndt_filename"))
        self.horizontalLayout.addWidget(self.lndt_filename)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.lbl_error = QtGui.QLabel(self.centralwidget)
        self.lbl_error.setObjectName(_fromUtf8("lbl_error"))
        self.horizontalLayout.addWidget(self.lbl_error)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.lbl_ip = QtGui.QLabel(self.centralwidget)
        self.lbl_ip.setObjectName(_fromUtf8("lbl_ip"))
        self.horizontalLayout.addWidget(self.lbl_ip)
        self.line_8 = QtGui.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtGui.QFrame.VLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.horizontalLayout.addWidget(self.line_8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_5 = QtGui.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.verticalLayout.addWidget(self.line_5)
        self.grPlot = PlotWidget(self.centralwidget)
        self.grPlot.setObjectName(_fromUtf8("grPlot"))
        self.verticalLayout.addWidget(self.grPlot)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ModMen® Production | EEG Server", None))
        self.pt_combo.setItemText(0, _translate("MainWindow", "Patient 1", None))
        self.pt_combo.setItemText(1, _translate("MainWindow", "Patient 2", None))
        self.ch_combo.setItemText(0, _translate("MainWindow", "Channel 0", None))
        self.ch_combo.setItemText(1, _translate("MainWindow", "Channel 1", None))
        self.ch_combo.setItemText(2, _translate("MainWindow", "Channel 2", None))
        self.ch_combo.setItemText(3, _translate("MainWindow", "Channel 3", None))
        self.ch_combo.setItemText(4, _translate("MainWindow", "Channel 4", None))
        self.ch_combo.setItemText(5, _translate("MainWindow", "Channel 5", None))
        self.ch_combo.setItemText(6, _translate("MainWindow", "Channel 6", None))
        self.ch_combo.setItemText(7, _translate("MainWindow", "Channel 7", None))
        self.lbl_error.setText(_translate("MainWindow", "Client Disconnected!", None))
        self.lbl_ip.setText(_translate("MainWindow", "IP", None))

from pyqtgraph import PlotWidget
