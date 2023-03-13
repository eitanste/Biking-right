# Biking-right
We're excited to share that we recently completed a unique project In collaboration with ALYN Hospital! Introducing Biking Right - a new project that aims to make biking more accessible for children with disabilities. One of the main challenges faced by children with disabilities is finding ways to participate in physical activities that are enjoyable and beneficial. Biking Right uses real-time input from a child's bike to create an interactive game that promotes both safe cycling techniques and rehabilitation of the injured leg. Moreover the Physiotherapist can adjust the difficulty of the game to meet the child's abilities. Biking Right helps kids to build confidence and strength while having fun.

In order to help them, we created a game that is controlled by an Arduino and two pressure sensors mounted on a bike's pedals using 3D printed adapters. The game involves a car that needs to avoid obstacles and collect fuel while moving forward as far as possible. The Arduino reads the pressure applied on each pedal and counts the number of successful pedal strokes in a row. This data is then transferred to a Python program using the serial port. The game will interact in real time with the data we get from the ports. 

We're proud to have developed Biking Right as a way to make biking more inclusive for all children. We’re thrilled with the results of this project and we learned a lot about programming and electronics in the process. Together, we can create a world where every child has the chance to enjoy the benefits of physical activity. We’re looking forward to exploring new projects in the future!

# Pedal-Powered Car Game
Welcome to the Pedal-Powered Car Game project! This is an Arduino-based 2D game that uses pressure sensors mounted on a bike's pedals to control a car that must avoid obstacles and collect fuel. This repository contains all the necessary files and instructions to run the project.

## Table of Contents
Prerequisites
Installation
Usage
Contributing


## Prerequisites
To use this project, you will need:

An Arduino board (tested on Arduino Uno R3)
Two pressure sensors (tested with FS-05)
Python 3.x installed on your computer
Pygame library for Python 3.x installed on your computer
(Optional) A 3D printed STL adapter for mounting the sensors on the pedals, which can improve performance.
*Note: If you don't have the 3D printed adapter, you can still mount the sensors on the pedals using other methods, such as zip ties or tape.

## Installation
To install the project, follow these steps:

Clone this Git repository onto your computer.
Connect your Arduino board to your computer.
Install the necessary Python libraries: pygame,random,serial.
Upload the pedal-powered-car.ino file to your Arduino board using the Arduino IDE.


## Installation
To install the project, follow these steps:

Clone this Git repository onto your computer.
Connect your Arduino board to your computer.
Connect the pressure sensors to the breadboard and connect the breadboard to the Arduino board using long wires.
(Optional) If you have the 3D printed adapter, mount the sensors on the pedals using the adapter.
Upload the pedal-powered-car.ino file to your Arduino board using the Arduino IDE.
Install the necessary Python libraries by running pip install -r requirements.txt in the terminal.

## Usage
To run the project, follow these steps:

Open a terminal and navigate to the cloned repository.
Run python main.py to start the game.
Make sure the bike pedals are properly connected to the pressure sensors and the Arduino board.
(Optional) If you have the 3D printed adapter, make sure the sensors are mounted on the pedals.
Start pedaling on the bike pedals to control the car.

Note: If the game is not responding to the pedal inputs, make sure the connections between the pressure sensors, breadboard, and Arduino board are correct. You can also check the serial monitor in the Arduino IDE to make sure the sensors are sending the correct data.

## Contributing
If you'd like to contribute to this project, please follow these guidelines:

Fork this repository.
Create a new branch for your changes.
Make your changes and commit them.
Push your changes to your forked repository.
Create a pull request to merge your changes into this repository.
