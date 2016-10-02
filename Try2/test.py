
from __future__ import print_function
from testTwitch import TwitchChatStream
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


validDirectionChar = ['r', 'l', 's']
validMovementChar = ['f', 'b']
directionCodes ={'rf' : 'forward right', 'rb' : 'backwards right', 'lf' : 'forward left', 'lb' : 'backwards left', 'sf' : 'straight', 'sb' : 'backwards'}

movementTime = 1 #CHANGE TO CHANGE MOVEMENT DISTANCE
start = time.time()
rf = 0
rb = 0
lf = 0
lb = 0
sf = 0
sb = 0

totalVotes = 0
winnerVotes = 0




def setLeft() : #27 left, 22 right
    GPIO.output(27, True)
    GPIO.output(22, False)

def setRight() :
    GPIO.output(27, False)
    GPIO.output(22, True)

def setStraight() :
    GPIO.output(27, True)
    GPIO.output(22, True)

def moveForward() : #23 forward, 24 back
   # print (time.asctime(time.localtime(time.time())))
    GPIO.output(23, True)
    GPIO.output(24, False)
    start = time.time()  
    timeout = start + movementTime
    while True :
        #print (time.asctime(time.localtime(time.time())))

        if time.time() > timeout :
            break
        if (not GPIO.input(10)) :
            print("Obstacle Detected!")
            break
    print("stopping")
    GPIO.output(23, True)
    GPIO.output(24, True)
    GPIO.output(27, True)
    GPIO.output(22, True)

def moveBackward() :
    GPIO.output(23, False)
    GPIO.output(24, True)
    time.sleep(movementTime)
    GPIO.output(23, True)
    GPIO.output(24, True)
    GPIO.output(27, True)
    GPIO.output(22, True)
        
    
def stop() :
    setStraight()
    GPIO.output(23, True)
    GPIO.output(24, True)
    GPIO.output(27, True)
    GPIO.output(22, True)

def processVote(direction, movement) :
    global rf, rb, lf, lb, sf, sb    
    if (direction == 'r' and movement == 'f') :
        rf = rf + 1
    elif (direction == 'r' and movement == 'b') :
        rb = rb + 1
    elif (direction == 'l' and movement == 'f') :
        lf = lf + 1
    elif (direction == 'l' and movement == 'b') :
        lb = lb + 1
    elif (direction == 's' and movement == 'f') :
        sf = sf + 1
    elif (direction == 's' and movement == 'b') :
        sb = sb + 1             
    
def maxVote() :
   global winnerVotes, totalVotes
   votes = {'rf': rf, 'rb': rb, 'lf': lf, 'lb': lb, 'sf' : sf, 'sb' : sb}
   winner = max(votes, key=votes.get)
   totalVotes = sum(votes.values())
   winnerVotes = max(votes.values())
   print("total votes: ", totalVotes)
   print("winner's votes: ", winnerVotes)
   #print(votes,'max votes: ', max(votes.values()))   
   if (max(votes.values()) == 0):
       winner = 'none'
   print(winner, 'wins')
   return winner

def movementPhase(move) :
    global directionCodes,winnerVotes, totalVotes
    if (move == 'none') :
        return    
#    samtxt = str("Moving ", directionCodes.get(move), "with ",winnerVotes," votes out of ",totalVotes," submissions!!")
    samtxt = str("Moving "+ str(directionCodes.get(move))+ " with "+str(winnerVotes)+" votes out of "+str(totalVotes)+" submissions!!")
    #chatstream.send_chat_message("Moving %s with %d votes out of %d submissions!!",directionCodes.get(move),winnerVotes,totalVotes)
    chatstream.send_chat_message(samtxt)
    
    print("Moved!")
    if (move[0] == 'r') :
        setRight()
    elif (move[0] == 'l') :
        setLeft()
    elif (move[0] == 's') :
        setStraight()

    if (move[1] == 'f') :
        moveForward()
    elif (move[1] == 'b') :
        moveBackward()

def resetToZero() :
    global rf, rb, lf, lb, sf, sb, start 
    print("Counter Reset!")       
    start = time.time()    
    rf = rb = lf = lb = sf = sb = 0
    chatstream.send_chat_message("Commands: RF (Right-Forward), LF (Left-Forward, SF (Straight), RB (Right-Backwards), LB (Left-Backwards, SB (Backwards)")



if __name__ == "__main__":
    # Launch a verbose (!) twitch stream
    with TwitchChatStream(username="hackumbcdrives",
                          oauth="oauth:6s0pnadvvzneyi94srek17ptr7l0ri",
                          verbose=True) as chatstream:

        # Send a message to this twitch stream
        chatstream.send_chat_message("hackUMBC Drives ONLINE")
        chatstream.send_chat_message("Commands: RF (Right-Forward), LF (Left-Forward, SF (Straight), RB (Right-Backwards), LB (Left-Backwards, SB (Backwards)")

        # Continuously check if messages are received (every ~10s)
        # This is necessary, if not, the chat stream will close itself
        # after a couple of minutes (due to ping messages from twitch)
        while True: #char at 15(r, l, or s) and 16 (f or b) index
            received = chatstream.twitch_receive_messages()
            if received:
                #print("received:", received)
                #print(received[0])            
                #print(type(received[0]))
                theStr = str(received)
                #print("String: ", theStr)
                #print(type(theStr))
                directionChar = theStr[15].lower()                 
                #print("Direction: ", directionChar)
                movementChar = theStr[16].lower()                
                #print("Movement: ", movementChar)                
                #print(directionChar == 'r')
                #print(movementChar == 'f')
                if (directionChar in validDirectionChar and 
                    movementChar in validMovementChar) :                
                    processVote(directionChar, movementChar)
                
            if time.time() > start + 5:
                movementPhase(maxVote())
                resetToZero()
                    
            #print("bracket test: ", received["message"])
            #str1 = ''.join(received)
            #print(str1)
            #print(type(received))
            #time.sleep(1)
            

            