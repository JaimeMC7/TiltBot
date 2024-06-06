# TiltBot
![TiltBot-image](Images/TiltBot.jpg)


## Index
- [Project description](#Project-description)
- [Structure](#Structure)
  - [Laberinth platform](#Laberinth-platform)
  - [Walls and plugs](#Walls-and-plugs)
- [Arquitecture](#Arquitecture)
  - [Action Module](#Action-Module)
    - [Action Hardware](#Action-Hardware)
    - [Action Software](#Action-Software)
  - [Vision Module](#Vision-Module)
    - [Vision Hardware](#Vision-Hardware)
    - [Vision Software](#Vision-Software)
    - [Limitations](#Vision-Limitations)
- [TO DOs](#TO-DOs)
- [References](#References)


## Project description
TiltBot is an entertainment device where you try to get a ball from one side of a maze to the opposite side, just by tilting it. Along the way, you'll need to dodge holes, or you'll have to start over!
Using it is simple: you can tilt the maze platform where the ball is located with a joystick.

If crossing the maze is too difficult, TiltBot has an extra feature. You can switch to an automatic mode, where AI will solve the maze, showing you one of the possible paths to the end. (For now, the algorithm is somewhat limited. See the Limitations section.)

Additionally, to increase the amount of fun, the maze format can be customized. You can open or close holes, as well as restructure the walls to choose your own difficulty.

## Structure
The structure is one of the most important parts of this project. To create a customizable maze, we had to come up with a structure that would allow us to rearrange where the walls that delimit the path of the maze should be, and the holes through which it should avoid falling. We designed the platform of our maze with holes where different pieces of walls fit and holes where plugs fit that allow the ball to pass over it. In addition to this, the structure has an exterior frame that will allow the platform to rotate on an axis. This has been achieved by means of a servomotor that will be attached to this frame by means of an elongated metal plate. As for the movement in the other axis of the inner platform, we have placed another servo attached to the bottom of the inner platform of the maze and joined to the outer frame by another plate. This allows us to obtain the desired movement in both axes.

<img src="Images/3D-platform-and-walls.jpg" alt="3D-platform-and-walls" width="400" height="300">

#### Laberinth platform
<img src="Images/3D-platform.jpg" alt="3D-platform" width="300" height="400">
We made a platform that has nine main isles of floor. Among them, four central X-shaped holes remain in the center of the platform, and eight small holes are located on the exterior side. Also, each piece of the floor has four holes in it, that can be fitted with our plugs in order to make the maze either easier or harder.


#### Walls and plugs
<img src="Images/3D-wall-pieces.jpg" alt="3D-wall-pieces" width="300" height="400">
We have designed different types of central walls, combining parts at ground level that let us create very varied mazes. For the exterior walls, we only have two types, ground level and wall lavel. Regarding the plugs, they are all the same, and they are of such a height that allows the ball to pass over it effortlessly.

#### 


## Arquitecture
For the operation of TiltBot, we have divided its components into two interconnected modules.

### Action Module
This module is the one in charge of the actual movement of the laberinth that allows the puzzle to be solved.

#### Action Hardware
In order to move the structure, we make use of two different servo motors, one for the outer layer, and the other for the inner layer. Each of this servos move in different directions, allowing the structure to tilt in any angle needed. For a deeper understanding check [Structure](#Structure).

To be able to control manually this servos we have also connected a joystick, which moves both motors acordingly to the direction and amount of preassure applied on it.

All of this is interconected by an Arduino UNO R3 module.


<img src="Action Module/Action Module circuit v1.png" alt="Action-module-HW-components" width="600" height="400">


#### Action Software


### Vision Module
#### Vision Hardware


#### Vision Software
*Dependencies*:
- OpenCV/cv2
- Numpy

#### Vision Limitations


## TO DOs
- [x] Design and assembly of the structure.
- [x] Calibrate the movement ranges of the platform's servomotors.
  - [x] In the code.
  - [x] Phisically.
- [x] Vision Module.
  - [x] Differentiate obstacles, ball, and maze path using a camera.
  - [x] Basic algorithm to solve the maze.
  - [x] Improve the solving algorithm.
  - [x] Calibrate commands to move the ball in the correct direction.
- [x] Communication between the vision module and the action module.


## References
- Original idea for the project by Antonio Álvarez: https://www.youtube.com/watch?v=PMSr5L0SD24
- Tutorial - Usage of Joysticks with Arduino: https://programarfacil.com/blog/arduino-blog/joystick-con-arduino/
- Tutorial - Usage of Servos with Arduino: https://programarfacil.com/blog/arduino-blog/servomotor-con-arduino/
- Tutorial - Send data from Arduino to Raspberry (Serial connection): https://www.youtube.com/watch?v=-3swby4ryU4
