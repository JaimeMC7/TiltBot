#define PIN_VRx A1
#define PIN_VRy A0
#define PIN_SW 2
 
// Includes y declaraciones de servo motores
#define PIN_SERVO_EXT 6
#define PIN_SERVO_INT 5

#include <Servo.h>
#include <Keyboard.h>


Servo servoExterior;
Servo servoInterior;


// Valores de entrada Joystick
int x, y;
// Angulos equivalentes
int x_ang, y_ang;


void setup(){
  
  // inicializar monitor serie a 9600 baudios
  Serial.begin(9600);
  analogReference(DEFAULT);

  //  Configuramos pin del pulsador del joystick como entrada con pullup
  pinMode( PIN_SW, INPUT_PULLUP );
  pinMode(PIN_VRx, INPUT); // Configurar el pin como entrada
  pinMode(PIN_VRx, INPUT); // Configurar el pin como entrada



	//Enlazamos el motor exterior al pin PIN_SERVO_EXT
	servoExterior.attach(PIN_SERVO_EXT);
  servoExterior.write(130);

	//Enlazamos el motor interior al pin PIN_SERVO_INT
	servoInterior.attach(PIN_SERVO_INT);
  servoInterior.write(123);
  

  
  
}

void loop(){
  

  
  /*
  // Lectura de caracteres desde el pc
  if (Serial.available()) {
    int key = Serial.read(); // Lee la tecla presionada
    
    // Realiza acciones basadas en la tecla presionada
    switch (key) {
      case 'w' :
         Serial.print( "ARRIBA \n" );
         y_ang = 110;
        break;
      case 'a' :
        Serial.print( "IZQUIERDA \n" );
        x_ang = 190;
        // Hacer algo cuando se presiona la tecla 'b'
        break;
      case 's' :
        Serial.print( "ABAJO \n" );
        y_ang = 70;
        // Hacer algo cuando se presiona la tecla 'a'
        break;
      case 'd' :
        Serial.print( "DERECHA \n" );
        x_ang = 45;
        // Hacer algo cuando se presiona la tecla 'b'
        break;
      case ' ':
        x_ang = 130;
        y_ang = 90;
        // Hacer algo cuando se presiona la tecla 'b'
        break;
      default:
        
        break;
      // Agrega más casos según las teclas que quieras detectar
    }
  }
  */
  ///// PUNTOS CLAVE:
  //x_ang = 130 --> horizontal
  //x_ang = 45 --> inclin borde mas proximo (der si lo miras de frente)
  //x_ang = 180 --> inclin lado contrario (izq si lo miras de frente)



  // Posiciones del joystick
  x = analogRead(PIN_VRx);
  y = analogRead(PIN_VRy);
  // Mapeo de los valores a grados (0-180)

  
  x_ang = map( x, 0, 1023, 45, 180 );
  y_ang = map( y, 0, 1023, 140, 100 );
  //y_ang = 100;//120 centro

  //Print de los valores en monitor serie
  
  Serial.print( "X_ang:" );
  Serial.print(x);
  Serial.print("  ");

  Serial.print( "Y_ang:" );
  Serial.print(y);

  // 0 pulsado -- 1 no pulsado
  Serial.print( " SW (Boton joystick):");
  Serial.print( digitalRead(PIN_SW) );
  Serial.println();
  

	//Desplazar motor exterior a x_angº
	
  servoExterior.write(x_ang);
  servoInterior.write(y_ang);
  

  //Esperar 1/4 de segundo (en milisegundos)
	//delay(2000);
  

}
