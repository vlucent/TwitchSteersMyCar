# Twitch Steers - HackUMBC F2016

This project was created at HackUMBC Fall2016 event.
We were inspired by the [Twitch Plays Pokemon](https://www.twitch.tv/twitchplayspokemon) stream.

The project involves the control of an off-the-shelf Remote Control toy car 
using commands typed in the chatbox of the [twitch stream](https://www.twitch.tv/hackumbcdrives).

<img src="https://raw.githubusercontent.com/vlucent/TwitchSteersMyCar/master/Images/example.png" height="200px">


The RC car and its controller was dissassembled to access the electronics inside.
It was quickly discovered that the car was controlled through digital inputs (push buttons for Forward/Reverse and a tri-state switch for Left-Straight-Right).

<img src="https://raw.githubusercontent.com/vlucent/TwitchSteersMyCar/master/Images/RC_CircuitBoard.jpg" height="200px">
(Original RC car circuit board)

The motors were rewired to a simple [L293DNE](http://www.ti.com/lit/ds/symlink/l293.pdf) motor control H-bridge IC to allow 5V logic control from the GPIO pins of a [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).
The Raspberry Pi was responsible for parsing messages for commands from the live Twitch stream, and executing the most-voted-for command, allowing the RC car to move in the indicated direction. The directions for moving the RC car was preserved from the original toy, so that it could move forward/backward with steering.

<img src="https://raw.githubusercontent.com/vlucent/TwitchSteersMyCar/master/Images/raspiWiring.jpg" height="200px">
(Raspberry Pi GPIO pins)

The result is a car, whose control is democratized to a web-enabled chat stream.

To try the script on your own project, run the [test.py](https://raw.githubusercontent.com/vlucent/TwitchSteersMyCar/master/src/test.py) script on your Raspberry Pi with the drive motors connected to GPIO pins 23 & 24, and steering connected to pins 27 & 22.
There is also a handy test [script](https://raw.githubusercontent.com/vlucent/TwitchSteersMyCar/master/src/testGPIO.py) to see if you wired the motors correctly.

# Challenges in this Project
There were several challenges that needed to be solved in order for full functionality.
The Raspi needed to fit in the chasis of the RC car along with the breadboard. THis caused us to dremmel and carve away material in the chasis so the the wiring could be routed inside the car. The raspi needed to fit in the car, but also have its hdmi and usb ports exposed for quick hot fixes that needed to be appplied.

# Improvements
Our project used a through-hole IC that needed a breadboard for wiring, which resulted in a larger amount of space just for wiring the Motor IC chip.
In the future the breadboard coud be replaced with a smaller breakout board(link) and a surface-mout(link) version of the motor controller. This assembly could then be campactly fit on top of the Rasperry Pi 3.

The Raspeberry Pi itself could be replaced with a Raspberry Pi Zero(link). This would trade-off the higher processing speed of the Pi3 for the slower processor on the Pi Zero. There would also be a lack of onboard wifi, though adding a wifi-card to the Pi Zero is possible and has been done(link) before. The Pi Zero and the breakout board could then be tucked neatly inside the Rc car with no need for physical modifications
# License

MIT