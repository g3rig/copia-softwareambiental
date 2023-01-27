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

class customSerialB(QObject):

	data_available_MUL_2 = pyqtSignal(str)
	data_availableP2TMT1 = pyqtSignal(str)
	data_availableP2TMT2 = pyqtSignal(str)
	data_availableP2TMT3 = pyqtSignal(str)
	data_availableP2TMT4 = pyqtSignal(str)
	data_availableP2TMT5 = pyqtSignal(str)
	data_availableP2TMT6 = pyqtSignal(str)
	data_availableP2TT1 = pyqtSignal(str)
	data_availableP2TT2 = pyqtSignal(str)
	data_availableP2TT3 = pyqtSignal(str)
	data_availableP2TT4 = pyqtSignal(str)
	data_availableP2TT5 = pyqtSignal(str)
	data_availableP2TT6 = pyqtSignal(str)
	data_availableP2TT7 = pyqtSignal(str)
	data_availableCO2Au = pyqtSignal(str)
	data_availableTempAu = pyqtSignal(str)
	data_availableHRAu = pyqtSignal(str)

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



	def connect_serialB(self):
		
		self.start_threadB()


	def read_serialB(self):
		time.sleep(0.2)

		try:
			self.serialPort.open()
			time.sleep(1)
			print("MUL_2 CONECTADO")

		except:
			print("MUL_2 FALLÓ AL CONECTAR A PUERTO")
		time.sleep(2)

		while (self.alive.isSet() and self.serialPort.is_open):
			try:
				#global configComandos
				#consultamos BA
				time.sleep(1.5)
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAA=str(configuracion['COMANDOS']['COBA']) + "\r"
					self.serialPort.write(comandoAA.encode())

				time.sleep( 0.5 )
				#leemos BA...
				data1 = self.serialPort.readline().decode("utf-8").strip()
				#print(data1)
				if(len(data1)>1):
					xA=definirvalores2(data1)
					#print("xA")
					
					self.data_available_MUL_2.emit("MUL_2 CONECTADO")

					self.data_availableP2TMT1.emit(xA[0])
					self.data_availableP2TMT2.emit(xA[1])
					self.data_availableP2TMT3.emit(xA[2])
					self.data_availableP2TMT4.emit(xA[3])

					"""#------------datos con compensación----------
					CxA=[0,0,0,0]
					configuracion.read('configCompenB.cfg')
					pA=float(xA[0])+float(configuracion['COMPENB']['CO1'])
					CxA[0]=("{:.2f}".format(pA))
					
					pB=float(xA[1])+float(configuracion['COMPENB']['CO2'])
					CxA[1]=("{:.2f}".format(pB))
					
					pC=float(xA[2])+float(configuracion['COMPENB']['CO3'])
					CxA[2]=("{:.2f}".format(pC))
					
					pD=float(xA[3])+float(configuracion['COMPENB']['CO4'])
					CxA[3]=("{:.2f}".format(pD))
					"""


				
				#------------------------------------------------------------------------------------
				#consultamos BB
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAB=str(configuracion['COMANDOS']['COBB']) + "\r"
					self.serialPort.write(comandoAB.encode())

				time.sleep( 0.5 )
				#leemos BB...
				data2 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data2)>1):
					xB=definirvalores2(data2)
					#print("xB")
					self.data_availableP2TMT5.emit(xB[0])
					self.data_availableP2TMT6.emit(xB[1])
					self.data_availableP2TT1.emit(xB[2])
					self.data_availableP2TT2.emit(xB[3])

					"""#------------datos con compensación----------
					CxB=[0,0,0,0]
					configuracion.read('configCompenB.cfg')

					qA=float(xB[0])+float(configuracion['COMPENB']['CO5'])
					CxB[0]=("{:.2f}".format(qA))

					qB=float(xB[1])+float(configuracion['COMPENB']['CO6'])
					CxB[1]=("{:.2f}".format(qB))

					qC=float(xB[2])+float(configuracion['COMPENB']['CO7'])
					CxB[2]=("{:.2f}".format(qC))

					qD=float(xB[3])+float(configuracion['COMPENB']['CO8'])
					CxB[3]=("{:.2f}".format(qD))
					"""


				#------------------------------------------------------------------------------------
				#consultamos BC
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAC=str(configuracion['COMANDOS']['COBC']) + "\r"
					self.serialPort.write(comandoAC.encode())

				time.sleep( 0.5 )
				#leemos BC.
				data3 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data3)>1):
					xC=definirvalores2(data3)
					#print("xC")
					self.data_availableP2TT3.emit(xC[0])
					self.data_availableP2TT4.emit(xC[1])
					self.data_availableP2TT5.emit(xC[2])
					self.data_availableP2TT6.emit(xC[3])

					"""#------------datos con compensación----------
					CxC=[0,0,0,0]
					configuracion.read('configCompenB.cfg')

					rA=float(xC[0])+float(configuracion['COMPENB']['CO9'])
					CxC[0]=("{:.2f}".format(rA))

					rB=float(xC[1])+float(configuracion['COMPENB']['CO10'])
					CxC[1]=("{:.2f}".format(rB))

					rC=float(xC[2])+float(configuracion['COMPENB']['CO11'])
					CxC[2]=("{:.2f}".format(rC))

					rD=float(xC[3])+float(configuracion['COMPENB']['CO12'])
					CxC[3]=("{:.2f}".format(rD))
		"""


				#------------------------------------------------------------------------------------
				#consultamos BD
				
				if(self.serialPort.is_open):

					configuracion.read("/home/labcim/SoftwareAmbientalCITEC/Configuracion/configComandos.cfg")
					comandoAD=str(configuracion['COMANDOS']['COBD']) + "\r"
					self.serialPort.write(comandoAD.encode())

				time.sleep( 0.5 )
				#leemos BD.
				data4 = self.serialPort.readline().decode("utf-8").strip()
				if(len(data4)>1):
					xD=definirvalores2(data4)
					#print("xD")
					self.data_availableP2TT7.emit(xD[0])
					self.data_availableCO2Au.emit(xD[1])
					self.data_availableTempAu.emit(xD[2])
					self.data_availableHRAu.emit(xD[3])

					"""#------------datos con compensación----------
					CxD=[0,0,0,0]
					configuracion.read('configCompenB.cfg')

					sA=float(xD[0])+float(configuracion['COMPENB']['CO13'])
					CxD[0]=("{:.2f}".format(sA))

					sB=float(xD[1])+float(configuracion['COMPENB']['CO14'])
					CxD[1]=("{:.2f}".format(sB))
					#CxD[1]=(((CxD[1]-4)*2000)/16)

					sC=float(xD[2])+float(configuracion['COMPENB']['CO15'])
					CxD[2]=("{:.2f}".format(sC))
					#CxD[2]=(((CxD[1]-4)*2000)/16)

					sD=float(xD[3])+float(configuracion['COMPENB']['CO16'])
					CxD[3]=("{:.2f}".format(sD))
					#CxD[3]=(((CxD[1]-4)*2000)/16)
					
				
				if(len(data1)>1 and len(data2)>1 and len(data3)>1 and len(data4)>1):
					datatodos2=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + CxA[0] + " , " + CxA[1] + " , " + CxA[2] + " , " + CxA[3] + " , " + CxB[0] + " , " + CxB[1] + " , " + CxB[2] + " , " + CxB[3] + " , " + CxC[0] + " , " + CxC[1] + " , " + CxC[2] + " , " + CxC[3] + " , " + CxD[0] + " , " + CxD[1] + " , " + CxD[2] + " , " + CxD[3]
					print(datatodos2)
					escribir2(datatodos2)
					time.sleep(1)
					self.data_available_MUL_2_state2.emit(time.strftime("%H:%M:%S"))
					time.sleep( 0.5 )
					
				else:
					nodata2=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + " NO DATA "
					print(nodata2)
					escribir2(nodata2)

					self.data_available_MUL_2.emit("MUL_2 DESCONECTADO")
				"""
			except Exception as ex:
				print(ex)
				#guardado en errorlist.txt
				global errorlist
				archivo=open(errorlist,'a')
				archivo.write("SerialB:")
				archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
				archivo.write("\n")
				archivo.write(str(ex))
				archivo.write("\n")
				archivo.write("\n")
				archivo.close()
				time.sleep(1)



	def start_threadB(self):
		self.thread = Thread(target = self.read_serialB)
		self.thread.setDaemon(1)
		self.alive.set()
		self.thread.start()

