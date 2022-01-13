import sys
import typing

import numpy as np
import serial
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtWidgets import QDialog , QApplication
from PyQt5.uic import loadUi
import pygame
import time
import winsound
from gtts import gTTS
from playsound import playsound

motor="01"
direccion="0"
velocidad="00"
enable_send=False
joy_horizontal_enable=True
enable_velocidad_min=True
delay = 250
baudrate=115200
puerto="COM12"

vel_min1="05"
vel_min2="11"
vel_min3="07"
vel_min4="03"
vel_min5="02"
vel_min6="04"

vel_max1="15"
vel_max2="20"
vel_max3="07"
vel_max4="07"
vel_max5="02"
vel_max6="06"

tts = gTTS('hombro', lang='es')
with open("hombro.mp3", "wb") as archivo:
    tts.write_to_fp(archivo)

tts2 = gTTS('base', lang='es')
with open("base.mp3", "wb") as archivo2:
    tts2.write_to_fp(archivo2)

tts3 = gTTS('codo', lang='es')
with open("codo.mp3", "wb") as archivo3:
    tts3.write_to_fp(archivo3)

tts4 = gTTS('muñeca', lang='es')
with open("mu.mp3", "wb") as archivo4:
    tts4.write_to_fp(archivo4)

tts5 = gTTS('giro pinza', lang='es')
with open("giro_mu.mp3", "wb") as archivo5:
    tts5.write_to_fp(archivo5)

tts6 = gTTS('pinza', lang='es')
with open("pinza.mp3", "wb") as archivo6:
	tts6.write_to_fp(archivo6)

tts7 = gTTS('Atencion... atencion.... Procedimiento de autodestrucción iniciado ', lang='es')
with open("mensaje_juego.mp3", "wb") as archivo7:
	tts7.write_to_fp(archivo7)

class tehseencode(QMainWindow):
	def __init__(self):
		global uart, motor, baudrate
		super(tehseencode,self).__init__()
		loadUi("hd_gui5.ui", self)
		#self.setStyleSheet("background-color: black;")
		self.statusBar().showMessage("Bienvenid@")
		#self.showMaximized()
		self.show()
		self.setWindowTitle("HARDWARE DEBUGGER")

		self.conect_label.setText('CONECTANDO')
		self.baudrate_label.setText(str(baudrate))
		self.puerto_label.setText(puerto)
		# self.conect_label.setStyleSheet("background-color: rgb(243, 244, 169); color: black")
		self.conect_label.setFont(QFont('Arial', 16))
		#self.SHOW.clicked.connect(self.onClicked)
		#self.CAPTURE.clicked.connect(self.CaptureClicked)

		uart = serial.Serial(puerto, baudrate)
		self.joystick()
	@pyqtSlot()
	def joystick(self):
		global uart, direccion, velocidad, enable_send, motor, joy_horizontal_enable, enable_velocidad_min
		####### Initialise the pygame library #######
		try:
			pygame.init()
			# Connect to the first JoyStick
			j = pygame.joystick.Joystick(0)
			j.init()
			analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
			self.TEXT.setText('Joystick Inicializado : %s' % j.get_name())
			# print('Initialized Joystick : %s' % j.get_name())
		except:
			self.TEXT.setText('No se inicializó joystick')
		#############################
		self.conect_label.setText('CONECTADO')
		self.conect_label.setFont(QFont('Arial', 18))
		count = 0
		count2 = 0
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.JOYBUTTONDOWN:
					if event.button == 0:
						print("x")
						self.indicador_motor()
						self.base_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						motor = "01"
						joy_horizontal_enable=True
						playsound("base1.mp3")
					if event.button == 1:
						print("circulo")
						self.indicador_motor()
						self.hombro_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						motor = "02"
						joy_horizontal_enable = False
						playsound("hombro1.mp3")
					if event.button == 2:
						print("cuadrado")
						self.indicador_motor()
						self.codo_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						motor = "03"
						joy_horizontal_enable = False
						playsound("codo1.mp3")
					if event.button == 3:
						print("triangulo")
						self.indicador_motor()
						self.mu_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						motor = "04"
						joy_horizontal_enable = False
						playsound("mu1.mp3")
					if event.button == 5:
						print("ps")
						playsound("mensaje_juego.mp3")
					if event.button == 11:
						print("Flecha hacia arriba")
						self.indicador_motor()
						self.giro_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						self.TEXT.setText("Boton FLECHA ARRIBA")
						motor = "05"
						joy_horizontal_enable = True
						playsound("giro_mu1.mp3")
					if event.button == 12:
						print("Flecha hacia abajo")
						self.indicador_motor()
						self.pinza_label.setStyleSheet("background-color: rgb(255, 255, 0); color: black")
						self.TEXT.setText('Boton FLECHA Abajo')
						motor = "06"
						joy_horizontal_enable = True
						playsound("pinza1.mp3")

				if event.type == pygame.JOYBUTTONUP:
					print("Button Released")
					enable_send=False

				if event.type == pygame.JOYAXISMOTION:
					analog_keys[event.axis] = event.value
					if joy_horizontal_enable:
						if enable_velocidad_min:
							self.velocidad_min()
						else:
							self.velocidad_max()
						#print(analog_keys[2]) ##### 2: Right Analog Horizontal
						if analog_keys[2] > 0 and analog_keys[2] <= 0.25 :
							print("00000")
							direccion = "1"
							enable_send=False
						if analog_keys[2] > 0.25:
							print("AAAAA")
							direccion = "1"
							enable_send = True

						if analog_keys[2] < 0 and analog_keys[2] >= -0.25:
							print("1111")
							direccion = "0"
							enable_send = False
						if analog_keys[2] < -0.25:
							print("CCCC")
							direccion = "0"
							enable_send = True

					else:
						## 3: Right Analog Vertical
						if analog_keys[3] > 0 and analog_keys[3] <= 0.25 :
							print("2222")
							direccion = "0"
							enable_send = False
						if analog_keys[3] > 0.25:
							print("EEEE")
							direccion = "0"
							enable_send = True

						if analog_keys[3] < 0 and analog_keys[3] >= -0.25:
							print("3333")
							direccion = "1"
							enable_send = False
						if analog_keys[3] < -0.25:
							print("GGGGG")
							direccion = "1"
							enable_send = True

					# Triggers
					if analog_keys[4] > 0 or analog_keys[5] > 0 :  # Left trigger and Right Trigger
						print("009")
						enable_velocidad_min=False
						self.velocidad_max()
					if analog_keys[4] < 0 or analog_keys[5] < 0 :
						print("00A")
						enable_velocidad_min=True
						self.velocidad_min()

			if enable_send:
				count=count+1
				MESSAGE ="$MECA,"+motor+",00,A,"+direccion+","+velocidad+"\r\n"
				uart.write(str.encode(MESSAGE))
				self.send_listWidget.insertItem(0,MESSAGE[0:18])
				if count >10:
					count=0
					#self.send_listWidget.takeItem(1)
					self.send_listWidget.clear()
			else:
				count2 = count2 + 1
				velocidad="00"
				direccion="0"
				MESSAGE = "$MECA," + motor + ",00,A," + direccion + "," + velocidad + "\r\n"
				#MESSAGE = "$MECA," + motor + ",00,A," + direccion + ",00\r\n"
				#self.send_listWidget.addItem(MESSAGE[0:18])
				self.send_listWidget.insertItem(0, MESSAGE[0:18])
				uart.write(str.encode(MESSAGE))
				if count2 >10:
					count2=0
					#self.send_listWidget.takeItem(1)
					self.send_listWidget.clear()

			loop = QEventLoop()
			QTimer.singleShot(delay, loop.quit)
			loop.exec_()
				#print(MESSAGE)
	def indicador_motor(self):
		self.hombro_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")
		self.base_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")
		self.codo_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")
		self.mu_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")
		self.giro_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")
		self.pinza_label.setStyleSheet("background-color: rgb(240, 240, 240); color: black")

	def velocidad_null(self):
		global velocidad
		velocidad = "00"

	def velocidad_min(self):
		global velocidad, motor
		if motor == "01":
			velocidad = vel_min1
		if motor == "02":
			velocidad = vel_min2
		if motor == "03":
			velocidad = vel_min3
		if motor == "04":
			velocidad = vel_min4
		if motor == "05":
			velocidad = vel_min5
		if motor == "06":
			velocidad = vel_min6

	def velocidad_max(self):
		global velocidad, motor
		if motor == "01":
			velocidad = vel_max1
		if motor == "02":
			velocidad = vel_max2
		if motor == "03":
			velocidad = vel_max3
		if motor == "04":
			velocidad = vel_max4
		if motor == "05":
			velocidad = vel_max5
		if motor == "06":
			velocidad = vel_max6

app =  QApplication(sys.argv)
window=tehseencode()
window.show()
#window.showFullScreen() #showFullScreen()

try:
	sys.exit(app.exec_())
except:
	print('excitng')
