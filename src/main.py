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

movementTime = 1

def setLeft() : #27 left, 22 right
    GPIO.output(27, True)
    GPIO.output(22, False)

def setRight() :
    GPIO.output(27, False)
    GPIO.output(22, True)

def setStraight() :
    GPIO.output(27, False)
    GPIO.output(22, False)

def moveFoward() : #23 forward, 24 back
    GPIO.output(23, True)
    GPIO.output(24, False)
    time.sleep(movementTime)
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
    GPIO.output(23, True)
    GPIO.output(24, False)
    
# Parse Twitch

myUsername = "HackUMBCdrives";
myKey = "oauth:6s0pnadvvzneyi94srek17ptr7l0ri";

# opens up Twitch
with TwitchChatStream(username = myUsername,
                      oauth = myKey,
                      verbose = True) as chatstream:
    chatstream.send_chat_message("I'm in the chat");
    # Gets new messages for 5 seconds
    start = time.time();
    dirVote = {"lf": 0 , "lb":0, "ls": 0 , "rb":0, "rf": 0 , "sb":0};

    while True:
        msg = chatstream.twitch_receive_messages()
        print("just in: ",msg);
        parsedMsg = ''.join(msg[''.join(msg).find("message") + 5:]);
        if msg: print("received: ",parsedMsg);
            
        if len(parsedMsg) == 2: dirVote[parsedMsg] = dirVote[parsedMsg] + 1;

        if time.time() > start + 5:
            # Get the max and execute
            maxDir = max(dirVote.iteritems(), key=operator.itemgetter(1))[0];
            if maxDir == 0: break;
            if maxDir[0] == 'r':
                finCmd = "r";
		setRight();
            elif maxDir[0] == 'l':
                finCmd = "l";
		setLeft();
            elif maxDir[0] == 's': 
                finCmd = "s";
		setStraight();
            if maxDir[1] == 'f': 
                finCmd += "f"
		moveForward();
            elif maxDir[1] == 'b': 
                finCmd += "b"
		moveBackward();
                
            # resets the values to next loop
            start = time.time();
            dirVote = {"lf": 0 , "lb":0, "ls": 0 , "rb":0, "rf": 0 , "sb":0};

            # Send a message to this twitch stream
            chatstream.send_chat_message(finCmd);
