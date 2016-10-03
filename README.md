# Twitch Steers - HackUMBC F2016

This project was created at HackUMBC Fall2016 event.
We were inspired by the [Twitch Plays Pokemon](https://www.twitch.tv/twitchplayspokemon) stream.

The project involves the control of an off-the-shelf Remote Control toy car 
using commands typed in the chatbox of the [twitch stream](https://www.twitch.tv/hackumbcdrives).

The RC car and its controller was dissassembled to access the electronics inside.
It was quickly discovered that the car was controlled through digital inputs (push buttons for Forward/Reverse and a tri-state switch for Left-Straight-Right).

The motors were rewired to a simple [L293DNE](http://www.ti.com/lit/ds/symlink/l293.pdf) motor control H-bridge IC to allow 5V logic control from the GPIO pins of a [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).
The Raspberry Pi was responsible for parsing messages for commands from the live Twitch stream, and executing the most-voted-for command, allowing the RC car to move in the indicated direction. The directions for moving the RC car was preserved from the original toy, so that it could move forward/backward with steering.

The result is a car. whose control is democratized to a web-enabled chat stream

