# TiltBot
![TiltBot-image](Images/TiltBot.jpg)


## Indíce
- [Descripción del proyecto](#Descripción-del-proyecto)
- [Estructura](#Estructura)
  - [Plataforma del laberinto](#Plataforma-del-laberinto)
  - [Paredes y tapones](#Paredes-y-tapones)
- [Arquitectura](#Arquitectura)
  - [Módulo de acción](#Módulo-de-acción)
    - [Action Hardware](#Action-Hardware)
    - [Action Software](#Action-Software)
  - [Módulo de visión](#Módulo-de-visión)
    - [Vision Hardware](#Vision-Hardware)
    - [Vision Software](#Vision-Software)
    - [Limitaciones](#Vision-Limitations)
- [TO DOs](#TO-DOs)
- [Referencias](#Referencias)


## Descripción del proyecto
TitlBot es un dispositivo de entretenimiento en el que has de intentar conseguir 
llevar una bola desde un lado de un laberinto hasta el lado opuesto, tan solo 
inclinandolo. Por el camino deberás de ir esquivando los agujeros, ¡o te tocará
volver a empezar!
La forma de usarlo es simple: mediante un joystick puedes inclinar la plataforma 
del laberinto en el que se encuentra la bola. 

Si cruzar el laberinto se te hace dificil, TiltBot tiene una funcionalidad extra. 
Puedes cambiar a un modo automático, en el que mediante IA 
se resolverá el laberinto, mostrandote uno de los posibles caminos hacia 
el final. (Por el momento el algoritmo es algo limitado. Vease en el apartado [Limitaciones](#Vision-Limitations) )

Además, para aumentar la cantidad de diversión, el formato del laberinto puede
personalizarse. Puedes abrir o cerrar agujeros, así como reestructurar las paredes
para elegir tu propia dificultad.


## Estructura
La estructura es una de las partes de mayor importancia en este proyecto.

#### Plataforma del laberinto

#### Paredes y tapones

####  


## Arquitectura
Para el funcionamiento de TiltBot hemos dividido sus componentes en dos modulos interconectados

### Módulo de acción
#### Action Hardware
<img src="Action Module/Action Module circuit v1.png" alt="Action-module-HW-components" width="600" height="400">


#### Action Software


### Módulo de visión
#### Vision Hardware


#### Vision Software
*Dependencias*:
- OpenCV/cv2 [MODIFICAR POR LA LIBRERIA USADA]
- Numpy

#### Vision Limitations


## TO DOs
- [x] Diseño y montaje de la estructura.
- [x] Calibrar rangos de desplazamiento de los servomotores de la plataforma del laberinto.
  - [x] En el codigo
  - [x] Fisicamente 
- [ ] Módulo de visión.
  - [x] Diferenciar obstaculos, bola y camino del laberinto con cámara.
  - [x] Algoritmo basico para resolver el laberinto.
  - [ ] Mejorar el algoritmo de resolución.
  - [ ] Calibrar ordenes para desplazar la bola en la dirección correcta.
- [ ] Comunicación entre modulo de visión y de acción


## Referencias
- Idea original del proyecto, por Antonio Álvarez: https://www.youtube.com/watch?v=PMSr5L0SD24
- Tutorial - Uso de Joysticks en Arduino: https://programarfacil.com/blog/arduino-blog/joystick-con-arduino/
- Tutorial - Uso de Servos en Arduino: https://programarfacil.com/blog/arduino-blog/servomotor-con-arduino/
- Tutorial - Send data from Arduino to Raspberry (Serial connection): https://www.youtube.com/watch?v=-3swby4ryU4
- 


