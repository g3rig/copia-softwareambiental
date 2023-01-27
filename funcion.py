import RPi.GPIO as GPIO
import time

def compara1(actual, deseado):
    if actual>deseado:
        print("cierra ventila auditorio")
        cierravau()
        
    elif actual<deseado:
        print("abre ventila auditorio")
        abrevau()
        
    else:
        print("se mantiene como esta")


def compara2(actual, deseado):
    if actual>deseado:
        print("cierra ventila Multiuso")
        cierravmu()
        
    elif actual<deseado:
        print("abre ventila Multiuso")
        abrevmu()
        
    else:
        print("se mantiene como esta")


def compara3(actual, deseado):
    if actual>deseado:
        print("abre extractor")
        abreein()
        abreees()
        
    elif actual<deseado:
        print("cierra extractor")
        cierraein()
        cierraees()
        
    else:
        print("se mantiene como esta") 


def compara4(actual, deseado):
    if actual>deseado:
        print("abre extractor secretaria")
        abreese()
        abreees()
        
    elif actual<deseado:
        print("cierra extractor secretaria")
        cierraese()
        cierraees
        
    else:
        print("se mantiene como esta")

#--------------------abre por alto co2 -------------------------
def ggMu():
    print("abre Multiuso por alto co2")
    abreemu()
    abreees()

#----------------funciones abre-----------
def abrevau():
    #pin abre
    LED_PIN = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(17)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abrevmu():
    #pin abre
    LED_PIN = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(27)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abrevte():
    #pin abre 
    LED_PIN = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(22)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abreemu():
    #pin abre
    LED_PIN = 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(5)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abreein():
    #pin abre
    LED_PIN = 6
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(6)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abreese():
    #pin abre
    LED_PIN = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(19)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

def abreees():
    #pin abre
    LED_PIN = 26

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(26)
    if state==0:
        b=0
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)

#-----------------------funciones cierra------------------

def cierravau():
    #pin cierra
    LED_PIN = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(17)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierravmu():
    #pin cierra
    LED_PIN = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(27)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierravte():
    #pin cierra
    LED_PIN = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(22)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierraemu():
    #pin cierra
    LED_PIN = 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(5)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierraein():
    #pin cierra
    LED_PIN = 6

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(6)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierraese():
    #pin cierra
    LED_PIN = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(19)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)

def cierraees():
    #pin cierra
    LED_PIN = 26

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    state = GPIO.input(26)
    if state==1:
        b=1
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)




        
        
    
