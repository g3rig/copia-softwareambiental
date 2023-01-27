import time
from datetime import datetime
#------------------------------MUL 1--------------------------------------


def checkfile(archivo):
	try:
		fichero = open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+archivo)
		fichero.close()

	except:
		fichero = open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+archivo,'w')
		fichero.close()



def escribir(datatodos):
	actual=datetime.now()
	mes=str(actual.month)
	año=str(actual.year)
	MUL_1="MUL_1_"+mes+"_"+año+".txt"
	checkfile(MUL_1)
	archivo=open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+MUL_1,'a')
	archivo.write(datatodos)
	archivo.write("\n")
	archivo.close()

#------------------------------MUL 2--------------------------------------

MUL_2="MUL_2.txt"
def checkfile2(archivo):
	try:
		fichero = open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+archivo)
		fichero.close()

	except:
		fichero = open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+archivo,'w')
		fichero.close()



def escribir2(datatodos):
	actual2=datetime.now()
	mes2=str(actual2.month)
	año2=str(actual2.year)
	MUL_2="MUL_2_"+mes2+"_"+año2+".txt"
	checkfile(MUL_2)
	archivo=open("/home/labcim/SoftwareAmbientalCITEC/Datos/"+MUL_2,'a')
	archivo.write(datatodos)
	archivo.write("\n")
	archivo.close()

