# Roomba for Scratch

This project is to provide an easy-to-use extension to the Scratch project (https://scratch.mit.edu) for controlling the Roomba cleanning robots so our kids can use Scratch to create fun projects with Roomba robots.

To control the Roomba robot we need to connect a controller to it via its 7-pin mini-DIN port, and connect Scratch to this controller using Scratch's extension system.

Currently the program code is being developped using Raspberry Pi Model 3 B+. However, the aim is to put all hardware specific code inside a hardware abstraction layer so other part of the project can be re-used on different controller hardwares.

The Roomba robot used for this development is currently a retired Roomba 565. Its Open Interface specification can be found under "tech-specifications" folder. Likewise, the communication via Open Interface will be isolated in another HAL.

As this project seems to be the first of the kind on GitHub (e.g. search Roomba+Scratch did not return any result), collaboration and contribution are very welcome!

