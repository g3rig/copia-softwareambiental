import serial, serial.tools.list_ports
import time
from threading import Thread, Event
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from convertidor import *
from atxt import *
import configparser
#from Direcciones import *

configuracion = configparser.ConfigParser()
errorlist="errorlist.txt"
#configComandos="/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg"



class customSerialA(QObject):

	data_available_MUL_1 = pyqtSignal(str)
	data_availableP1TMT1 = pyqtSignal(str)
	data_availableP1TMT2 = pyqtSignal(str)
	data_availableP1TMT3 = pyqtSignal(str)
	data_availableP1TMT4 = pyqtSignal(str)
	data_availableP1TP1 = pyqtSignal(str)
	data_availableP1TP2 = pyqtSignal(str)
	data_availableP1TP3 = pyqtSignal(str)
	data_availableP1TP4 = pyqtSignal(str)
	data_availableP1TP5 = pyqtSignal(str)
	data_availableP1TL1 = pyqtSignal(str)
	data_availableP1TS3 = pyqtSignal(str)
	data_availableP1TS1 = pyqtSignal(str)
	data_availableP1TS2 = pyqtSignal(str)
	data_availableP2CO2_2 = pyqtSignal(str)
	data_availableP1CO2_1 = pyqtSignal(str)
	data_availableP2CO2_1 = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.serialPort = serial.Serial()
		self.serialPort.timeout = 0.5


		self.baudratesDIC = {
		'1200':1200,
		'2400':2400,
		'4800':4800,
		'9600':9600,
		'19200':19200,
		'38400':38400,
		'57600':57600,
		'115200':115200
		}
		self.portList = []

		#Hilos
		self.thread = None 
		self.alive = Event()



	def connect_serialA(self):
		
		self.start_threadA()


	def read_serialA(self):


		try:
			self.serialPort.open()
			time.sleep(1)
			print("MUL_1 CONECTADO")
			band=1

		except:
			print("MUL_1 FALLÓ AL CONECTAR A PUERTO")
			band=0
		time.sleep(2)

		while (self.alive.isSet() and self.serialPort.is_open and band==1):
			try:
				#global configComandos
				#consultamos AA
				time.sleep(1.5)
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAA=str(configuracion['COMANDOS']['COAA']) + "\r"
					self.serialPort.write(comandoAA.encode())

				time.sleep( 0.5 )
				#leemos AA...
				data1 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data1)>1):
					xA=definirvalores(data1)
					#print("xA")
					self.data_available_MUL_1.emit("MUL_1 CONECTADO")
					
					self.data_availableP1TMT1.emit(xA[0])
					self.data_availableP1TMT2.emit(xA[1])
					self.data_availableP1TMT3.emit(xA[2])
					self.data_availableP1TMT4.emit(xA[3])

					"""#------------datos con compensación----------
					CxA=[0,0,0,0]
					configuracion.read('configCompenA.cfg')

					pA=float(xA[0])+float(configuracion['COMPENA']['CO1'])
					CxA[0]=("{:.2f}".format(pA))

					pB=float(xA[1])+float(configuracion['COMPENA']['CO2'])
					CxA[1]=("{:.2f}".format(pB))

					pC=float(xA[2])+float(configuracion['COMPENA']['CO3'])
					CxA[2]=("{:.2f}".format(pC))

					pD=float(xA[3])+float(configuracion['COMPENA']['CO4'])
					CxA[3]=("{:.2f}".format(pD))
					"""


				
				#------------------------------------------------------------------------------------
				#consultamos AB
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAB=str(configuracion['COMANDOS']['COAB']) + "\r"
					self.serialPort.write(comandoAB.encode())

				time.sleep( 0.5 )
				#leemos AB...
				data2 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data2)>1):
					xB=definirvalores(data2)
					#print("xB")
					self.data_availableP1TP1.emit(xB[0])
					self.data_availableP1TP2.emit(xB[1])
					self.data_availableP1TP3.emit(xB[2])
					self.data_availableP1TP4.emit(xB[3])

					"""#------------datos con compensación----------
					CxB=[0,0,0,0]
					configuracion.read('configCompenA.cfg')

					qA=float(xB[0])+float(configuracion['COMPENA']['CO5'])
					CxB[0]=("{:.2f}".format(qA))

					qB=float(xB[1])+float(configuracion['COMPENA']['CO6'])
					CxB[1]=("{:.2f}".format(qB))

					qC=float(xB[2])+float(configuracion['COMPENA']['CO7'])
					CxB[2]=("{:.2f}".format(qC))

					qD=float(xB[3])+float(configuracion['COMPENA']['CO8'])
					CxB[3]=("{:.2f}".format(qD))
					"""


				#------------------------------------------------------------------------------------
				#consultamos AC
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAC=str(configuracion['COMANDOS']['COAC']) + "\r"
					self.serialPort.write(comandoAC.encode())

				time.sleep( 0.5 )
				#leemos AC.
				data3 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data3)>1):
					xC=definirvalores(data3)
					#print("xC")
					self.data_availableP1TP5.emit(xC[0])
					self.data_availableP1TL1.emit(xC[1])
					self.data_availableP1TS3.emit(xC[2])
					self.data_availableP1TS1.emit(xC[3])

					"""#------------datos con compensación----------
					CxC=[0,0,0,0]
					configuracion.read('configCompenA.cfg')

					rA=float(xC[0])+float(configuracion['COMPENA']['CO9'])
					CxC[0]=("{:.2f}".format(rA))

					rB=float(xC[1])+float(configuracion['COMPENA']['CO10'])
					CxC[1]=("{:.2f}".format(rB))

					rC=float(xC[2])+float(configuracion['COMPENA']['CO11'])
					CxC[2]=("{:.2f}".format(rC))

					rD=float(xC[3])+float(configuracion['COMPENA']['CO12'])
					CxC[3]=("{:.2f}".format(rD))
					"""
					
				#------------------------------------------------------------------------------------
				#consultamos AD
				
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAD=str(configuracion['COMANDOS']['COAD']) + "\r"
					self.serialPort.write(comandoAD.encode())

				time.sleep( 0.5 )
				#leemos AD.
				data4 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data4)>1):
					xD=definirvalores(data4)
					#print("xD"+ data4)
					self.data_availableP1TS2.emit(xD[0])
					self.data_availableP2CO2_2.emit(xD[1])
					self.data_availableP1CO2_1.emit(xD[2])
					self.data_availableP2CO2_1.emit(xD[3])

					"""#------------datos con compensación----------
					CxD=[0,0,0,0]
					configuracion.read('configCompenA.cfg')

					sA=float(xD[0])+float(configuracion['COMPENA']['CO13'])
					CxD[0]=("{:.2f}".format(sA))

					sB=float(xD[1])+float(configuracion['COMPENA']['CO14'])
					CxD[1]=("{:.2f}".format(sB))
					#CxD[1]=(((CxD[1]-4)*2000)/16)

					sC=float(xD[2])+float(configuracion['COMPENA']['CO15'])
					CxD[2]=("{:.2f}".format(sC))

					sD=float(xD[3])+float(configuracion['COMPENA']['CO16'])
					CxD[3]=("{:.2f}".format(sD))
				
				if(len(data1)>1 and len(data2)>1 and len(data3)>1 and len(data4)>1):
					datatodos=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + CxA[0] + " , " + CxA[1] + " , " + CxA[2] + " , " + CxA[3] + " , " + CxB[0] + " , " + CxB[1] + " , " + CxB[2] + " , " + CxB[3] + " , " + CxC[0] + " , " + CxC[1] + " , " + CxC[2] + " , " + CxC[3] + " , " + CxD[0] + " , " + CxD[1] + " , " + CxD[2] + " , " + CxD[3]
					print(datatodos)
					escribir(datatodos)
					time.sleep(1)
					self.data_available_MUL_1_state.emit(time.strftime("%d/%m/%Y"))
					time.sleep( 0.5 )
					
				else:
					nodata=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + " NO DATA "
					print(nodata)
					escribir(nodata)

					self.data_available_MUL_1.emit("MUL_1 DESCONECTADO")
					"""
			except Exception as ex:
				print(ex)
				#guardado en errorlist.txt
				global errorlist
				archivo=open(errorlist,'a')
				archivo.write("SerialA:")
				archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
				archivo.write("\n")
				archivo.write(str(ex))
				archivo.write("\n")
				archivo.write("\n")
				archivo.close()
				time.sleep(1)




	def start_threadA(self):
		self.thread = Thread(target = self.read_serialA)
		self.thread.setDaemon(1)
		self.alive.set()
		self.thread.start()
