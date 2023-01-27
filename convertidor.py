
import struct
import binascii
import serial, serial.tools.list_ports
from threading import Thread, Event
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot


def definirvalores(d):

	separado=separar(d) #se obiene 4 valores

	return separado


#Aqui se separa los datos y se indivizualizan en una cadena de 4 valores
def separar(x):

	cadena=x
	
	g1=cadena[12:20]
	g2=cadena[21:29]
	g3=cadena[30:38]
	g4=cadena[39:47]

	uno="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g1))[0])
	dos="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g2))[0])
	tres="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g3))[0])
	cuatro="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g4))[0])

	separado=[uno,dos,tres,cuatro]
	return separado

#------------------------convertidor MUL 2-------------------------------

def definirvalores2(d):

	separado=separar(d) #se obiene 4 valores

	return separado


#Aqui se separa los datos y se indivizualizan en una cadena de 4 valores
def separar2(x):

	cadena=x
	
	g1=cadena[12:20]
	g2=cadena[21:29]
	g3=cadena[30:38]
	g4=cadena[39:47]

	uno="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g1))[0])
	dos="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g2))[0])
	tres="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g3))[0])
	cuatro="{0:.2f}".format(struct.unpack('>f', binascii.unhexlify(g4))[0])

	separado=[uno,dos,tres,cuatro]
	return separado













		
