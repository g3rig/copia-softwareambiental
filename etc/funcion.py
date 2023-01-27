import RPi.GPIO as GPIO
import time

def compara1(actual, deseado):
    
    LED_PIN = 17

    GPIO.setmode(GPIO.BCM)
    if actual>deseado:
        print("abre ventila")
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)
        
    elif actual<deseado:
        print("cierra ventila")
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.1)
        
    else:
        print("se mantiene como esta")


def compara2(actual, deseado):

    if actual>deseado:
        print("abre ventila")

    elif actual<deseado:
        print("cierra ventila")

    else:
        print("se mantiene como esta") 


def compara3(actual, deseado):

    if actual>deseado:
        print("abre ventila")

    elif actual<deseado:
        print("cierra ventila")

    else:
        print("se mantiene como esta")  


def compara4(actual, deseado):

    if actual>deseado:
        print("abre ventila")

    elif actual<deseado:
        print("cierra ventila")

    else:
        print("se mantiene como esta")


#-- Pin---
"""
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(0.1)


GPIO.output(LED_PIN, GPIO.LOW)
time.sleep(0.1)
"""



        
        
    
