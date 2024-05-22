# TiltBot
![TiltBot-image](Images/TiltBot.jpg)


## Indíce
- [Descripción del proyecto](#Descripción-del-proyecto)
- [Estructura](#Estructura)
  - [Plataforma del laberinto](#Plataforma-del-laberinto)
  - [Paredes y tapones](#Paredes-y-tapones)
- [Arquitectura](#Arquitectura)
  - [Módulo de acción](#Módulo-de-acción)
    - [Hardware](#Hardware)
    - [Software](#Software)
  - [Módulo de visión](#Módulo-de-visión)
    - [Hardware](#Hardware)
    - [Software](#Software)
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
el final.

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
#### Hardware
![Action-module-HW-components](Images/Action-Module/HW-components.jpg)


#### Software


### Módulo de visión
#### Hardware


#### Software
*Dependencias*:
- OpenCV/cv2 [MODIFICAR POR LA LIBRERIA USADA]

## TO DOs
- Probar diferentes rangos de desplazamiento de los servos de la plataforma del laberinto.
- Módulo de visión.
  - Diferenciar obstaculos, bola y camino del laberinto con cámara.
  - Algoritmo para resolver el laberinto.
  - Calibrar ordenes para desplazar la bola en la dirección correcta.


## Referencias
- Idea original del proyecto, por Antonio Álvarez: https://www.youtube.com/watch?v=PMSr5L0SD24
- Tutorial - Uso de Joysticks en Arduino: https://programarfacil.com/blog/arduino-blog/joystick-con-arduino/
- Tutorial - Uso de Servos en Arduino: https://programarfacil.com/blog/arduino-blog/servomotor-con-arduino/



