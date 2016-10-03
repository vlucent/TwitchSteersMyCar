import argparse
import time
import numpy as np
import operator
from testTwitch import TwitchChatStream
import time
import RPi.GPIO as GPIO

# Moving the car

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT) #Left
GPIO.setup(22, GPIO.OUT) #Right
GPIO.setup(23, GPIO.OUT) #Forward
GPIO.setup(24, GPIO.OUT) #Backward
GPIO.setup(10, GPIO.IN) #Collision avoidance

movementTime = 2 #CHANGE TO CHANGE MOVEMENT DISTANCE

def setLeft() : #27 left, 22 right
    GPIO.output(27, True)
    GPIO.output(22, False)

def setRight() :
    GPIO.output(27, False)
    GPIO.output(22, True)

def setStraight() :
    GPIO.output(27, False)
    GPIO.output(22, False)

def moveForward() : #23 forward, 24 back
    print time.asctime( time.localtime(time.time()) )
    GPIO.output(23, True)
    GPIO.output(24, False)
    start = time.time()  
    timeout = start + movementTime
    while True :
        if time.time() > timeout :
            break
        if (not GPIO.input(10)) :
            print("Obstacle Detected!")
            break
    print("stopping")
    print time.asctime( time.localtime(time.time()) )
    GPIO.output(23, False)
    GPIO.output(24, False)

def moveBackward() :
    GPIO.output(23, False)
    GPIO.output(24, True)
    time.sleep(movementTime)
    GPIO.output(23, False)
    GPIO.output(24, False)
    
def stop() :
    setStraight()
    GPIO.output(23, False)
    GPIO.output(24, False)


while True:
    command = input("Direction?: ")
    if command == 1:
        setLeft()
        time.sleep(1)
        stop()
        
    elif command == 2:
        setRight()
        time.sleep(1)
        stop()
    elif command == 3:
        moveForward()
        time.sleep(1)
        stop()

    elif command == 4:
        moveBackward()
        time.sleep(1)
        stop()
    

