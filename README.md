# Laser-Guided-vehicle
This repo is for our FCOM project - Laser Guided Vehicle
![img_20180501_015322](https://user-images.githubusercontent.com/25399528/41093041-eeb1a8a0-6a67-11e8-848d-c59ff611ab2d.jpg)


![img_20180501_015433](https://user-images.githubusercontent.com/25399528/41093104-10719e1e-6a68-11e8-9f40-26636717fad1.jpg)

# Overview

Our laser guided vehicle detects a laser pointer on ground or surface and follows it. The laser can therefore, be used to move the 
vehicle in a particular direction. It avoids collision through an ultrasonic sensor.

# Components Required

* A smartphone with IP Webcam app installed on it.

* A laser pointer and a laptop.

* A chasis for the vehicle along with wheels

* An ultrasonic sensor, bread board(small) and jumper wires

* Bluetooth module -2 and Arduino-2

* 4 Motors and 2 motor controllers

# Working

# Stage-1

The smartphone is kept over the vehicle which sends the live video feed of the laser to a laptop. This is done using a wifi hotspot.

The laptop is where all the image processing is performed. The capturevideov2.py script uses opencv to detect the laser (its center and radius)

We first take a frame from the video, convert it to HSV format and then using appropriate masks, we can separate the contours to find the biggest one

and then using moments we can find the center and radius.

# Stage-2

Next stage involves identifying the position of the laser pointer on the screen of the smartphone. A smartphone screen can be divided 

into 4 regions- left,right, forward and backward as shown below.

//Add image here

If the laser pointer lies in the forward region we can send a command to the vehicle to move forward and likewise for other directions as well

# Stage-3

In this stage we send the command to vehicle. After deciding in which direction we need to move the vehicle we send chracters

'f'-forward, b='backward', 'l'-left and 'r'-right

Using an arduino and a bluetooth module at the laptop's end we send the data to the arduino-bluetooth pair at the Vehicle. The bluetooth 

module needs to be configured properly using AT commands. Make one of the modules slave and another one master. 

Now data can be received at the vehicle end. For moving the vehicle forward all the wheels should move clockwise and just the opposite 

for backward. For moving left, just move the right side wheels clockwise and likewise for right. The arduino code carRobot.ino performs this task

# Additional functions:

The vehicle stops on 's' command and in case laser in not in the range of smartphone camera, the vehicle moves anti clockwise to find the laser. The vehicle also stops in case it finds an obstacle infront of it.
