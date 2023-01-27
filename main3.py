from io import DEFAULT_BUFFER_SIZE
import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QTableWidgetItem
from PyQt5.QtCore import QTimer,QDateTime
from Tabs import *
from customSerialA import customSerialA
from customSerialB import customSerialB
import configparser
from funcion import *
from atxt import *
import serial, serial.tools.list_ports
from threading import Thread, Event
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from Direcciones import *
from database.conn_mysql import *

#variables GLOBALES
#configCompenA="/home/labcim/SoftwareAmbientalCITEC/Configuracion/configCompenA.cfg"
#configCompenB="/home/labcim/SoftwareAmbientalCITEC/Configuracion/configCompenB.cfg"


#mul_1
P1TMT1 ,P1TMT2  ,P1TMT3 ,P1TMT4 ,P1TP1 ,P1TP2 ,P1TP3 ,P1TP4 =0,0,0,0,0,0,0,0
P1TP5 ,P1TL1 ,P1TS3 ,P1TS1 ,P1TS2 ,P2CO2_2 ,P1CO2_1 ,P2CO2_1=0,0,0,0,0,9999,9999,9999

#mul_2
P2TMT1 ,P2TMT2 ,P2TMT3 ,P2TMT4 ,P2TMT5 ,P2TMT6 ,P2TT1 ,P2TT2 =0,0,0,0,0,0,0,0
P2TT3 ,P2TT4 ,P2TT5 ,P2TT6 ,P2TT7 ,CO2Au ,TempAu ,HRAu =0,0,0,0,0,9999,0,0

bandera=True
errorlist="errorlist.txt"
configuracion = configparser.ConfigParser()



class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread = None 
        self.alive = Event()
        #global configSwitch
        global configTemp
        
        self.ui.label.setStyleSheet("background-color: red;")
        self.ui.label_2.setStyleSheet("background-color: red;")
        #versión
        self.ui.version.setText("Versión: 1.0")
        """
        configuracion.read(configSwitch)
        #manual/auto
        
        if (configuracion['SWITCH']['estado'])=="OFF":
            self.ui.checkBox.setChecked(False)
        else:
            self.ui.checkBox.setChecked(True)
        """
        self.ui.checkBox.setChecked(False)
        
        self.ui.temAoficinas2.setText("No Disp.")
        self.ui.temAoficinas2.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
        """
        #--------------------------------declaracion en UI de combobox tab_1-------------------------
        #Control manual
        self.ui.Pcmv_auditorio.setCurrentIndex(self.ui.Pcmv_auditorio.findText(configuracion['SWITCH']['vau'], QtCore.Qt.MatchFixedString))
        self.ui.Pcmv_biblioteca.setCurrentIndex(self.ui.Pcmv_biblioteca.findText(configuracion['SWITCH']['vmu'], QtCore.Qt.MatchFixedString))
        self.ui.Pcmv_techo.setCurrentIndex(self.ui.Pcmv_techo.findText(configuracion['SWITCH']['vte'], QtCore.Qt.MatchFixedString))
        self.ui.Pcme_biblioteca.setCurrentIndex(self.ui.Pcme_biblioteca.findText(configuracion['SWITCH']['emu'], QtCore.Qt.MatchFixedString))
        self.ui.Pcme_ingenieria.setCurrentIndex(self.ui.Pcme_ingenieria.findText(configuracion['SWITCH']['ein'], QtCore.Qt.MatchFixedString))
        self.ui.Pcme_secretaria.setCurrentIndex(self.ui.Pcme_secretaria.findText(configuracion['SWITCH']['ese'], QtCore.Qt.MatchFixedString))
        self.ui.Pcme_escaleras.setCurrentIndex(self.ui.Pcme_escaleras.findText(configuracion['SWITCH']['ees'], QtCore.Qt.MatchFixedString))
        """
        #T°
        configuracion.read(configTemp)
        self.ui.interCom.setCurrentIndex(self.ui.interCom.findText(configuracion['TEMP']['tp'], QtCore.Qt.MatchFixedString))
        self.ui.temDauditorio.setCurrentIndex(self.ui.temDauditorio.findText(configuracion['TEMP']['td1'], QtCore.Qt.MatchFixedString))
        self.ui.temDbiblioteca.setCurrentIndex(self.ui.temDbiblioteca.findText(configuracion['TEMP']['td2'], QtCore.Qt.MatchFixedString))
        #self.ui.temDoficinas2.setCurrentIndex(self.ui.temDoficinas2.findText(configuracion['TEMP']['td3'], QtCore.Qt.MatchFixedString))
        #self.ui.temDoficinas1.setCurrentIndex(self.ui.temDoficinas1.findText(configuracion['TEMP']['td4'], QtCore.Qt.MatchFixedString))

        #Co2
        #self.ui.PcCd_auditorio.setCurrentIndex(self.ui.PcCd_auditorio.findText(configuracion['TEMP']['cd1'], QtCore.Qt.MatchFixedString))
        self.ui.PcCd_biblioteca.setCurrentIndex(self.ui.PcCd_biblioteca.findText(configuracion['TEMP']['cd2'], QtCore.Qt.MatchFixedString))
        self.ui.PcCd_ingenieria.setCurrentIndex(self.ui.PcCd_ingenieria.findText(configuracion['TEMP']['cd3'], QtCore.Qt.MatchFixedString))
        self.ui.PcCd_secretaria.setCurrentIndex(self.ui.PcCd_secretaria.findText(configuracion['TEMP']['cd4'], QtCore.Qt.MatchFixedString))

        #-----------------------------------CONEXION MUL_1-----------------------------------------

        self.serialA = customSerialA()
        self.conectarA()
        time.sleep(0.5)
        
        self.serialA.data_available_MUL_1.connect(self.update_MUL_1)
        self.serialA.data_availableP1TMT1.connect(self.update_terminalP1TMT1)
        self.serialA.data_availableP1TMT2.connect(self.update_terminalP1TMT2)
        self.serialA.data_availableP1TMT3.connect(self.update_terminalP1TMT3)
        self.serialA.data_availableP1TMT4.connect(self.update_terminalP1TMT4)
        self.serialA.data_availableP1TP1.connect(self.update_terminalP1TP1)
        self.serialA.data_availableP1TP2.connect(self.update_terminalP1TP2)
        self.serialA.data_availableP1TP3.connect(self.update_terminalP1TP3)
        self.serialA.data_availableP1TP4.connect(self.update_terminalP1TP4)
        self.serialA.data_availableP1TP5.connect(self.update_terminalP1TP5)
        self.serialA.data_availableP1TL1.connect(self.update_terminalP1TL1)
        self.serialA.data_availableP1TS3.connect(self.update_terminalP1TS3)
        self.serialA.data_availableP1TS1.connect(self.update_terminalP1TS1)
        self.serialA.data_availableP1TS2.connect(self.update_terminalP1TS2)
        self.serialA.data_availableP2CO2_2.connect(self.update_terminalP2CO2_2)
        self.serialA.data_availableP1CO2_1.connect(self.update_terminalP1CO2_1)
        self.serialA.data_availableP2CO2_1.connect(self.update_terminalP2CO2_1)
        

        #-----------------------------------CONEXION MUL_2-----------------------------------------

        self.serialB = customSerialB()
        self.conectarB()
        
        self.serialB.data_available_MUL_2.connect(self.update_MUL_2)
        self.serialB.data_availableP2TMT1.connect(self.update_terminalP2TMT1)
        self.serialB.data_availableP2TMT2.connect(self.update_terminalP2TMT2)
        self.serialB.data_availableP2TMT3.connect(self.update_terminalP2TMT3)
        self.serialB.data_availableP2TMT4.connect(self.update_terminalP2TMT4)
        self.serialB.data_availableP2TMT5.connect(self.update_terminalP2TMT5)
        self.serialB.data_availableP2TMT6.connect(self.update_terminalP2TMT6)
        self.serialB.data_availableP2TT1.connect(self.update_terminalP2TT1)
        self.serialB.data_availableP2TT2.connect(self.update_terminalP2TT2)
        self.serialB.data_availableP2TT3.connect(self.update_terminalP2TT3)
        self.serialB.data_availableP2TT4.connect(self.update_terminalP2TT4)
        self.serialB.data_availableP2TT5.connect(self.update_terminalP2TT5)
        self.serialB.data_availableP2TT6.connect(self.update_terminalP2TT6)
        self.serialB.data_availableP2TT7.connect(self.update_terminalP2TT7)
        self.serialB.data_availableCO2Au.connect(self.update_terminalCO2Au)
        self.serialB.data_availableTempAu.connect(self.update_terminalTempAu)
        self.serialB.data_availableHRAu.connect(self.update_terminalHRAu)
        
        #------------------------------INICIO registro txt Mul 1--------------------------------------
        self.start_threadsave1()
        time.sleep(0.5)
        
        #------------------------------INICIO registro txt Mul 2--------------------------------------
        self.start_threadsave2()
        time.sleep(0.5)
        
        #------------------------------INICIO COMPARADOR--------------------------------------
        self.start_threadcomp()
        time.sleep(0.5)

        #------------------------------INICIO CONTROL MANUAL--------------------------------------
        self.start_threadmanual()
        time.sleep(0.5)

        #hora dinamica
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()


    #funcion de hora dinamica
    def showtime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString('dddd dd MMMM hh:mm:ss')
        texts = datetime.toString('hh:mm:ss dddd dd MMMM ')
        self.ui.label_3.setText("   "+ text)



    #---------------------------ESTADO MUL--------------------------------------------
    def update_MUL_1(self, data):
        self.ui.label.setText(data)
        if(data == "MUL_1 CONECTADO"):
            self.ui.label.setStyleSheet("background-color: lightgreen;")
        else:
            self.ui.label.setStyleSheet("background-color: red;")


    def update_MUL_2(self, data):
        self.ui.label_2.setText(data)
        if (data == "MUL_2 CONECTADO"):
            self.ui.label_2.setStyleSheet("background-color: lightgreen;")
        else:
            self.ui.label_2.setStyleSheet("background-color: red;")


    #----------------------------DEF TERMINALES A-------------------------------------
    #TMT
    def update_terminalP1TMT1(self, data):
        #config
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO1'])
        t=("{:.2f}".format(y))

        global P1TMT1
        P1TMT1=float(t)

        #dato piso
        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_3.setItem(0, 0, dato)
        
        #dato mux comp
         #valor leido
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(0, 2, dato2) 

         #comp
        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO1'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(0, 3, dato3)

         #valor final
        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(0, 4, dato4)
        
        #valor auditorio interior muro trombe
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 9, dato5)


    def update_terminalP1TMT2(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO2'])
        t=("{:.2f}".format(y))

        global P1TMT2
        P1TMT2=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_3.setItem(1, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(1, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO2'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(1, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(1, 4, dato4)

    def update_terminalP1TMT3(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO3'])
        t=("{:.2f}".format(y))

        global P1TMT3
        P1TMT3=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_3.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(2, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO3'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(2, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(2, 4, dato4)

    def update_terminalP1TMT4(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO4'])
        t=("{:.2f}".format(y))

        global P1TMT4
        P1TMT4=float(t)

        dato = QTableWidgetItem(str(t))
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_3.setItem(3, 0, dato)

        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(3, 2, dato2)

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO4'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(3, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(3, 4, dato4)
        
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 8, dato5)

    #TP
    def update_terminalP1TP1(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO5'])
        t=("{:.2f}".format(y))

        global P1TP1
        P1TP1=float(t)

        dato = QTableWidgetItem(str(t))
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_4.setItem(0, 0, dato)

        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(4, 2, dato2)

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO5'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(4, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(4, 4, dato4)

        #label oficina1TR
        self.ui.temAoficinas1.setText(str(t))
        #self.ui.PcTa_secretaria.setText(str(t))


    def update_terminalP1TP2(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO6'])
        t=("{:.2f}".format(y))

        global P1TP2
        P1TP2=float(t)

        dato = QTableWidgetItem(str(t))
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_4.setItem(1, 0, dato)

        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(5, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO6'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(5, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(5, 4, dato4)

    def update_terminalP1TP3(self, data):

        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO7'])
        t=("{:.2f}".format(y))

        global P1TP3
        P1TP3=float(t)

        dato = QTableWidgetItem(str(t))
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_4.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(6, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO7'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(6, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(6, 4, dato4)

    def update_terminalP1TP4(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO8'])
        t=("{:.2f}".format(y))

        global P1TP4
        P1TP4=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_4.setItem(3, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(7, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO8'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(7, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(7, 4, dato4)

    def update_terminalP1TP5(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO9'])
        t=("{:.2f}".format(y))

        global P1TP5
        P1TP5=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_4.setItem(4, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(8, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO9'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(8, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(8, 4, dato4)

    #TL
    def update_terminalP1TL1(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO10'])
        t=("{:.2f}".format(y))

        global P1TL1
        P1TL1=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_2.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(9, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO10'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(9, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(9, 4, dato4)

    #TS
    def update_terminalP1TS3(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO11'])
        t=("{:.2f}".format(y))

        global P1TS3
        P1TS3=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(10, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO11'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(10, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(10, 4, dato4)


    def update_terminalP1TS1(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO12'])
        t=("{:.2f}".format(y))

        global P1TS1
        P1TS1=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget.setItem(1, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(11, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO12'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(11, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(11, 4, dato4)

        #label auditorioTR
        self.ui.temAauditorio.setText(str(t))
        self.ui.PcTa_auditorio.setText(str(t))


    def update_terminalP1TS2(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO13'])
        t=("{:.2f}".format(y))

        global P1TS2
        P1TS2=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(12, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO13'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(12, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(12, 4, dato4)

    def update_terminalP2CO2_2(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO14'])
        t=("{:.2f}".format(y))

        global P2CO2_2
        P2CO2_2=float(t) #t=(((t-4)*2000)/16)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_12.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(13, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO14'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(13, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(13, 4, dato4)
        
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 1, dato5)

        #label Multiuso
        self.ui.Co2Abiblioteca.setText(str(t))
        self.ui.PcCa_biblioteca.setText(str(t))


    #C02
    def update_terminalP1CO2_1(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO15'])
        t=("{:.2f}".format(y))

        global P1CO2_1
        P1CO2_1=float(t) #t=(((t-4)*2000)/16)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_11.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(14, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO15'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(14, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(14, 4, dato4)

        #label auditorioTR
        self.ui.Co2Aoficinas1.setText(str(t))
        self.ui.PcCa_secretaria.setText(str(t))


    def update_terminalP2CO2_1(self, data):
        
        global configCompenA
        configuracion.read(configCompenA)
        y=float(data)+float(configuracion['COMPENA']['CO16'])
        t=("{:.2f}".format(y))

        global P2CO2_1
        P2CO2_1=float(t) #t=(((t-4)*2000)/16)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_13.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(15, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENA']['CO16'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(15, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C.setItem(15, 4, dato4)


        #label ingieneria
        self.ui.Co2Aoficinas2.setText(str(t))
        self.ui.PcCa_ingenieria.setText(str(t))
        



    #----------------------------DEF TERMINALES B-------------------------------------
    #TMT
    def update_terminalP2TMT1(self, data):

        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO1'])
        t=("{:.2f}".format(y))

        global P2TMT1
        P2TMT1=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(0, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO1'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(0, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(0, 4, dato4)
        
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 0, dato5)


    def update_terminalP2TMT2(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO2'])
        t=("{:.2f}".format(y))

        global P2TMT2
        P2TMT2=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(1, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(1, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO2'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(1, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(1, 4, dato4)

    def update_terminalP2TMT3(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO3'])
        t=("{:.2f}".format(y))

        global P2TMT3
        P2TMT3=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(2, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO3'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(2, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(2, 4, dato4)

    def update_terminalP2TMT4(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO4'])
        t=("{:.2f}".format(y))

        global P2TMT4
        P2TMT4=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(3, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(3, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO4'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(3, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(3, 4, dato4)
        
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 3, dato5)
    
    def update_terminalP2TMT5(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO5'])
        t=("{:.2f}".format(y))

        global P2TMT5
        P2TMT5=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(4, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(4, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO5'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(4, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(4, 4, dato4)

    def update_terminalP2TMT6(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO6'])
        t=("{:.2f}".format(y))

        global P2TMT6
        P2TMT6=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_6.setItem(5, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(5, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO6'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(5, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(5, 4, dato4)

    #TT
    def update_terminalP2TT1(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO7'])
        t=("{:.2f}".format(y))

        global P2TT1
        P2TT1=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(6, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO7'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(6, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(6, 4, dato4)

        #label bibliotecaTR
        self.ui.temAbiblioteca.setText(str(t))
        self.ui.PcTa_biblioteca.setText(str(t))



    def update_terminalP2TT2(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO8'])
        t=("{:.2f}".format(y))

        global P2TT2
        P2TT2=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(1, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(7, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO8'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(7, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(7, 4, dato4)

    def update_terminalP2TT3(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO9'])
        t=("{:.2f}".format(y))

        global P2TT3
        P2TT3=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(8, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO9'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(8, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(8, 4, dato4)

    def update_terminalP2TT4(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO10'])
        t=("{:.2f}".format(y))

        global P2TT4
        P2TT4=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(3, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(9, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO10'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(9, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(9, 4, dato4)

    def update_terminalP2TT5(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO11'])
        t=("{:.2f}".format(y))

        global P2TT5
        P2TT5=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(4, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(10, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO11'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(10, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(10, 4, dato4)

    def update_terminalP2TT6(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO12'])
        t=("{:.2f}".format(y))

        global P2TT6
        P2TT6=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(5, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(11, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO12'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(11, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(11, 4, dato4)

    def update_terminalP2TT7(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO13'])
        t=("{:.2f}".format(y))

        global P2TT7
        P2TT7=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_5.setItem(6, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(12, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO13'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(12, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(12, 4, dato4)

    #CO2Au
    def update_terminalCO2Au(self, data):

        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO14'])
        t=("{:.2f}".format(y))

        global CO2Au
        CO2Au=float(t) #t=(((t-4)*2000)/16)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_10.setItem(0, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(13, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO14'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(13, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(13, 4, dato4)
        
        dato5 = QTableWidgetItem(str(t))
        dato5.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_8.setItem(0, 10, dato5)

        #label auditorioTR
        self.ui.Co2Aauditorio.setText(str(t))
        #self.ui.PcCa_auditorio.setText(str(t))


    #TempAu
    def update_terminalTempAu(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO15'])
        t=("{:.2f}".format(y))

        global TempAu
        TempAu=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        #self.ui.tableWidget_8.setItem(2, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(14, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO15'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(14, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(14, 4, dato4)


    def update_terminalHRAu(self, data):
        
        global configCompenB
        configuracion.read(configCompenB)
        y=float(data)+float(configuracion['COMPENB']['CO16'])
        t=("{:.2f}".format(y))

        global HRAu
        HRAu=float(t)

        dato = QTableWidgetItem(str(t)) 
        #print (t)
        dato.setTextAlignment(QtCore.Qt.AlignCenter)
        #self.ui.tableWidget_8.setItem(3, 0, dato)
        
        dato2 = QTableWidgetItem(data)
        dato2.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(15, 2, dato2) 

        dato3 = QTableWidgetItem(configuracion['COMPENB']['CO16'])
        dato3.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(15, 3, dato3)

        dato4 = QTableWidgetItem(str(t))
        dato4.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_C_2.setItem(15, 4, dato4)
    


    def conectarA(self):
        #/dev/ttyUSB0
        self.serialA.serialPort.port = "/dev/ttyUSB0"
        self.serialA.connect_serialA()
        
          

    def conectarB(self ):
        #/dev/ttyUSB1
        self.serialB.serialPort.port = "/dev/ttyUSB1"
        self.serialB.connect_serialB()



    #---------------------------Hilo Comparador---------------------

    def comp(self):
        time.sleep(20)
        while (True) :
            try:
                #guarda tiempo de pausa de comparador y datos deseados en archivo respaldo config.cfg
                configuracion['TEMP']['td1'] = str(self.ui.temDauditorio.currentText())
                configuracion['TEMP']['td2'] = str(self.ui.temDbiblioteca.currentText())
                configuracion['TEMP']['cd2'] = str(self.ui.PcCd_biblioteca.currentText())
                configuracion['TEMP']['cd3'] = str(self.ui.PcCd_ingenieria.currentText())
                configuracion['TEMP']['cd4'] = str(self.ui.PcCd_secretaria.currentText())
                configuracion['TEMP']['tp'] = str(self.ui.interCom.currentText())
                global configTemp
                with open(configTemp, 'w') as archivo:
                    configuracion.write(archivo)

                if(self.ui.checkBox.isChecked()==True):
                    switch=True
                    self.ui.label_estado.setText("DESACTIVADO")
                    self.ui.label_estado.setStyleSheet("color: red;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                else:
                    switch=False
                    self.ui.label_estado.setText("ACTIVADO")
                    self.ui.label_estado.setStyleSheet("color: green;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    

                #pausa
                pausaDeseado=float(self.ui.interCom.currentText())
                #control
                if(switch==False):
                    #led CA activado
                    self.ui.ledCA.setStyleSheet("background-color: lightgreen;")
                    #------------------------------------auditorio------------------------------
                    #solo control t°
                    if float(P1TS1)!=0: #temAuditorio es P1TS1

                        datoactual=float(P1TS1)
                        datodeseado=float(self.ui.temDauditorio.currentText())

                        print("-------------",datoactual,"vs",datodeseado,"-------------")
                        compara1(datoactual,datodeseado)

                    #--------------------------------------multiuso-----------------------------
                    #control t° y co2
                    if float(P2CO2_2)!=9999 and float(P2CO2_2)<float(self.ui.PcCd_biblioteca.currentText()):
                        if float(P2TT1)!=0:

                            datoactual2=float(P2TT1)
                            datodeseado2=float(self.ui.temDbiblioteca.currentText())

                            print("-------------",datoactual2,"vs",datodeseado2,"-------------")
                            compara2(datoactual2,datodeseado2)

                    if float(P2CO2_2)>=float(self.ui.PcCd_biblioteca.currentText()):

                        ggMu()

                    #--------------------------------------ingieneria------------------------------
                    #solo control co2
                    if float(P2CO2_1)!=9999 and float(P2CO2_1)<float(self.ui.PcCd_ingenieria.currentText()):
                        if float(P2CO2_2)!=0: 

                            datoactual3=float(P2CO2_2)
                            datodeseado3=float(self.ui.PcCd_ingenieria.currentText())

                            print("-------------",datoactual3,"vs",datodeseado3,"-------------")
                            compara3(datoactual3,datodeseado3)

                    #--------------------------------------secretaria--------------------------------
                    #solo control co2
                    if float(P1CO2_1)!=9999 and float(P1CO2_1)<float(self.ui.PcCd_secretaria.currentText()):
                        if float(P1TP1)!=0:

                            datoactual4=float(P1CO2_1)
                            datodeseado4=float(self.ui.PcCd_secretaria.currentText())

                            print("-------------",datoactual4,"vs",datodeseado4,"-------------")
                            compara4(datoactual4,datodeseado4)

                    print(pausaDeseado)
                    aux=pausaDeseado-0.5
                    time.sleep(aux)
                    self.ui.ledCA.setStyleSheet("background-color: green;")
                    time.sleep(0.5)
                else:
                    #ledCA desactivado
                    self.ui.ledCA.setStyleSheet("background-color: red;")
                    time.sleep(1)
            except Exception as ex:
                print(ex)
                #ledCa error
                self.ui.ledCA.setStyleSheet("background-color: blue;")
                #guardado en errorlist.txt
                global errorlist
                archivo=open(errorlist,'a')
                archivo.write("comparador:")
                archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
                archivo.write("\n")
                archivo.write(str(ex))
                archivo.write("\n")
                archivo.write("\n")
                archivo.close()
                time.sleep(1)

    #-----------------------------------------Hilo Control Manual----------------------------------
    def manual(self):
        time.sleep(20)
        while (True) :
            #comparador fecha de ventila techo
            iverano= datetime(2020, 10, 1)
            fverano= datetime(2020, 3, 1)
            actual=datetime.now()

            if(actual.month==iverano.month):
                print("abre ventila techo")
                abrevte()

            elif(actual.month==fverano.month):
                print("cierra ventila techo")
                cierravte()
            """
            global configSwitch
            configuracion.read(configSwitch)
            #guardado en txt ----------------------
            configuracion['SWITCH']['vau'] = str(self.ui.Pcmv_auditorio.currentText())
            configuracion['SWITCH']['vmu'] = str(self.ui.Pcmv_biblioteca.currentText())
            configuracion['SWITCH']['vte'] = str(self.ui.Pcmv_techo.currentText())
            configuracion['SWITCH']['emu'] = str(self.ui.Pcme_biblioteca.currentText())
            configuracion['SWITCH']['ein'] = str(self.ui.Pcme_ingenieria.currentText())
            configuracion['SWITCH']['ese'] = str(self.ui.Pcme_secretaria.currentText())
            configuracion['SWITCH']['ees'] = str(self.ui.Pcme_escaleras.currentText())
            """
            if(self.ui.checkBox.isChecked()==True):
                switch=True
                #configuracion['SWITCH']['estado'] = "ON"
            else:
                switch=False
                #configuracion['SWITCH']['estado'] = "OFF"


            with open(configSwitch, 'w') as archivo:
                    configuracion.write(archivo)
            
            if(switch==True):
                try:
                    #led CM activo
                    self.ui.ledCM.setStyleSheet("background-color: lightgreen;")
                    #activa o desactiva ventolas/estractores dependiendo de la opcion colocada en combobox
                    #----vau
                    if (configuracion['SWITCH']['vau']=="on"):
                        abrevau()
                        self.ui.Pcmvl_auditorio.setText("ON")
                        self.ui.Pcmvl_auditorio.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierravau()
                        self.ui.Pcmvl_auditorio.setText("OFF")
                        self.ui.Pcmvl_auditorio.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    
                    #----vmu
                    if (configuracion['SWITCH']['vmu']=="on"):
                        abrevmu()
                        self.ui.Pcmvl_biblioteca.setText("ON")
                        self.ui.Pcmvl_biblioteca.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierravmu()
                        self.ui.Pcmvl_biblioteca.setText("OFF")
                        self.ui.Pcmvl_biblioteca.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")

                    #----vte
                    if (configuracion['SWITCH']['vte']=="on"):
                        abrevte()
                        self.ui.Pcmvl_techo.setText("ON")
                        self.ui.Pcmvl_techo.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierravte()
                        self.ui.Pcmvl_techo.setText("OFF")
                        self.ui.Pcmvl_techo.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")

                    #----emu
                    if (configuracion['SWITCH']['emu']=="on"):
                        abreemu()
                        self.ui.Pcmel_biblioteca.setText("ON")
                        self.ui.Pcmel_biblioteca.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierraemu()
                        self.ui.Pcmel_biblioteca.setText("OFF")
                        self.ui.Pcmel_biblioteca.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")

                    #----ein
                    if (configuracion['SWITCH']['ein']=="on"):
                        abreein()
                        self.ui.Pcmel_ingenieria.setText("ON")
                        self.ui.Pcmel_ingenieria.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierraein()
                        self.ui.Pcmel_ingenieria.setText("OFF")
                        self.ui.Pcmel_ingenieria.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")

                    #----ese
                    if (configuracion['SWITCH']['ese']=="on"):
                        abreese()
                        self.ui.Pcmel_secretaria.setText("ON")
                        self.ui.Pcmel_secretaria.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierraese()
                        self.ui.Pcmel_secretaria.setText("OFF")
                        self.ui.Pcmel_secretaria.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    
                    #----ees
                    if (configuracion['SWITCH']['ees']=="on"):
                        abreees()
                        self.ui.Pcmel_escaleras.setText("ON")
                        self.ui.Pcmel_escaleras.setStyleSheet("background-color: lightgreen;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    else:
                        cierraees()
                        self.ui.Pcmel_escaleras.setText("OFF")
                        self.ui.Pcmel_escaleras.setStyleSheet("background-color: orange;font: Segoi UI;font-weight: bold;qproperty-alignment: AlignCenter;")
                    time.sleep(1)
                except Exception as ex:
                    print(ex)
                    #led cm desactivado
                    self.ui.ledCM.setStyleSheet("background-color: blue;")
                    #guardado en errorlist.txt
                    global errorlist
                    archivo=open(errorlist,'a')
                    archivo.write("manual:")
                    archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
                    archivo.write("\n")
                    archivo.write(str(ex))
                    archivo.write("\n")
                    archivo.write("\n")
                    archivo.close()
                    time.sleep(1)
            else:
                #led cm desactivado
                self.ui.ledCM.setStyleSheet("background-color: red;")
                time.sleep(1)
    
    
    
    #---------------------------Hilo Guardado txt Mul 1---------------------


    def save1(self):
        time.sleep(10)
        while (True) :

            try:
                #guardado en txt
                datatodos=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + str(P1TMT1) + " , " + str(P1TMT2) + " , " + str(P1TMT3) + " , " + str(P1TMT4) + " , " + str(P1TP1) + " , " + str(P1TP2) + " , " + str(P1TP3) + " , " + str(P1TP4) + " , " + str(P1TP5) + " , " + str(P1TL1) + " , " + str(P1TS3) + " , " + str(P1TS1) + " , " + str(P1TS2) + " , " + str(P2CO2_2)  + " , " + str(P1CO2_1) + " , " + str(P2CO2_1)

                #Guardado en bd
                data_mul1 = (time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), float(P1TMT1), float(P1TMT2), float(P1TMT3), float(P1TMT4), float(P1TP1), float(P1TP2), float(P1TP3), float(P1TP4), float(P1TP5), float(P1TL1), float(P1TS3), float(P1TS1), float(P1TS2), float(P2CO2_2), float(P1CO2_1), float(P2CO2_1))

                #post_mul1(data_mul1)
                insert_mul1(data_mul1)



                print(datatodos)
                escribir(datatodos)
                self.ui.ledM1.setStyleSheet("background-color: lightgreen;")

                #pausa guardado datos en segundos-----------------------------------------------------------------------------
                global PausaGuardadoTxt
                time.sleep(PausaGuardadoTxt)

            except Exception as ex:
                print(ex)
                #ledM1 error
                self.ui.ledM1.setStyleSheet("background-color: blue;")
                #guardado en errorlist.txt
                global errorlist
                archivo=open(errorlist,'a')
                archivo.write("save1:")
                archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
                archivo.write("\n")
                archivo.write(str(ex))
                archivo.write("\n")
                archivo.write("\n")
                archivo.close()
                time.sleep(1)
    
    #---------------------------Hilo Guardado txt Mul 1---------------------
                
    def save2(self):
        time.sleep(10)
        while (True) :

            try:
                #guardado en txt
                datatodos2=time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S") + " , " + str(P2TMT1) + " , " + str(P2TMT2) + " , " + str(P2TMT3) + " , " + str(P2TMT4) + " , " + str(P2TMT5) + " , " + str(P2TMT6) + " , " + str(P2TT1) + " , " + str(P2TT2) + " , " + str(P2TT3) + " , " + str(P2TT4) + " , " + str(P2TT5) + " , " + str(P2TT6) + " , " + str(P2TT7) + " , " + str(CO2Au)  + " , " + str(TempAu) + " , " + str(HRAu)

                # Guardado en la bd
                data_mul2 = (time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), float(P2TMT1), float(P2TMT2), float(P2TMT3), float(P2TMT4), float(P2TMT5), float(P2TMT6), float(P2TT1), float(P2TT2), float(P2TT3), float(P2TT4), float(P2TT5), float(P2TT6), float(P2TT7), float(CO2Au), float(TempAu), float(HRAu))

                #post_mul2(data_mul2)
                insert_mul2(data_mul2)

                print(datatodos2)
                escribir2(datatodos2)
                self.ui.ledM2.setStyleSheet("background-color: lightgreen;")
                
                #pausa guardado datos en segundos-----------------------------------------------------------------------------
                global PausaGuardadoTxt
                time.sleep(PausaGuardadoTxt)
                
            except Exception as ex:
                print(ex)
                #ledM2 error
                self.ui.ledM2.setStyleSheet("background-color: blue;")
                #guardado en errorlist.txt
                global errorlist
                archivo=open(errorlist,'a')
                archivo.write("save2:")
                archivo.write(time.strftime("%d/%m/%Y")+ " , "  + time.strftime("%H:%M:%S"))
                archivo.write("\n")
                archivo.write(str(ex))
                archivo.write("\n")
                archivo.write("\n")
                archivo.close()
                time.sleep(1)
    
    def start_threadcomp(self):
        self.thread = Thread(target = self.comp)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def start_threadmanual(self):
        self.thread = Thread(target = self.manual)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        
    def start_threadsave1(self):
        self.thread = Thread(target = self.save1)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
    
    def start_threadsave2(self):
        self.thread = Thread(target = self.save2)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MiApp()
    w.show()
    sys.exit(app.exec_())
    