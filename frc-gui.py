#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc-gui.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the graphical user interface classes.
#################################################################################

import sys
from PyQt4 import QtGui, QtCore

from langauges import *
from frc_osx import *


lang = 'en-US'

class FRCDialog(QtGui.QWidget):
	
	def __init__(self):
                QtGui.QWidget.__init__(self)
                self.setGeometry(600, 400, 280, 100)
                self.setWindowTitle('FlyRodCrosbyOSX')
		self.setFixedSize(280, 100)
		label = QtGui.QLabel('Choose a language',self)
		label.move(20,20)
		l=["en-US",'fr', 'ar', 'es', "it", 'ru']

		self.ComboBox = QtGui.QComboBox(self)
		self.ComboBox.addItems(l)
		self.ComboBox.move(20,40)

		self.OkButton = QtGui.QPushButton('OK', self)
		self.OkButton.move(120,40)
		self.OkButton.clicked.connect(self.getLanguage)
		
		self.ExitButton = QtGui.QPushButton('exit', self)
		self.ExitButton.move(200,40)
             
                self.ExitButton.clicked.connect(self.exit)
        
	def exit(self):
                exit(0)
	
	def getLanguage(self):
		global lang
		lang = str(self.ComboBox.currentText())
		global Widget
		Widget  = FRCWidget()
		Widget.show()
		self.hide()

class FRCWidget(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setGeometry(300, 200, 1000, 400)
		self.setWindowTitle('FlyRodCrosby OSX')
		self.setFixedSize(1000, 400)
		first_msg=QtCore.QString.fromUtf8(First_msg(lang).getFirstMsg())
		label = QtGui.QLabel(first_msg,self)
		label.move(120,20)		
		border=20
		
		self.tbird_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(tbird_checkbox_msg(lang).getCheckBoxLabel()), self)			
		self.tbird_checkbox.move(20,border+60)

		self.tbb_checkbox  = QtGui.QCheckBox(QtCore.QString.fromUtf8(tbb_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.tbb_checkbox .move(20,border+90)

		self.torbirdy_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(torbirdy_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.torbirdy_checkbox.move(20,border+120)

		self.jitsi_checkbox  = QtGui.QCheckBox(QtCore.QString.fromUtf8(jitsi_checkbox_msg(lang).getCheckBoxLabel()), self)
               	self.jitsi_checkbox.move(20,border+150)

		self.truecrypt_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(truecrypt_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.truecrypt_checkbox.move(20,border+180)
		
		self.tailsISO_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(tailsISO_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.tailsISO_checkbox.move(20,border+210)

		self.fakeOut_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(fakeOut_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.fakeOut_checkbox.move(20,border+240)

		self.CryptoCat_checkbox = QtGui.QCheckBox(QtCore.QString.fromUtf8(CryptoCat_checkbox_msg(lang).getCheckBoxLabel()), self)
                self.CryptoCat_checkbox.move(20,border+270)



		self.OkButton = QtGui.QPushButton('OK', self)
		self.ExitButton = QtGui.QPushButton('exit', self)

		self.OkButton.move(400,350)
		self.ExitButton.move(480,350)
		self.OkButton.clicked.connect(self.action)
		self.ExitButton.clicked.connect(self.exit)

	def exit(self):
        	exit(0)

	def action(self):
		if self.tbird_checkbox.isChecked():
			getThunderbirdWithEnigmail(lang)
		if self.torbirdy_checkbox.isChecked():
			getTorBirdy()
            		installTorBirdy()
		if self.tbb_checkbox.isChecked():
			getTor(tor_url,lang) 
		if self.jitsi_checkbox.isChecked():
			getJitsi()
                if self.tailsISO_checkbox.isChecked():
			getTailsISO()
                if self.fakeOut_checkbox.isChecked():
			getFakeOut()
                if self.CryptoCat_checkbox.isChecked():
                        getCryptoCat()

# Main routine
app = QtGui.QApplication(sys.argv)
Dialog = FRCDialog()
Dialog.show()
sys.exit(app.exec_())
