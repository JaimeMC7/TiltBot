#define PIN_VRx A1
#define PIN_VRy A0
#define PIN_SW 2
 
// Includes y declaraciones de servo motores
#define PIN_SERVO_EXT 6
#define PIN_SERVO_INT 5

#include <Servo.h>
#include <Keyboard.h>

// Include para conexion serial con Raspberry Pi
#include <ArduinoJson.h>

Servo servoExterior;
Servo servoInterior;

// Valores centrales servomotores
int central_external_servo = 129;
int central_internal_servo = 121;


// Modo de juego
bool automatic = false;




// Enviar senal en serie
//
// Mensajes enviados:
//   200 --> empezar proceso automatico
//   300 --> siguiente punto
//   400 --> cancelar/acabar proceso
//



void serial_out(int value){

  //StaticJsonDocument<200> jsonDoc;
  //jsonDoc["value"] = value;
  //serializeJson(jsonDoc, Serial);

  Serial.print(value);
  Serial.println();

}


// Girar servomotores
void move(int x_ang, int y_ang){
  servoExterior.write(x_ang);
  servoInterior.write(y_ang);
}

// Todo el calculo automatico y comunicacion
void automatic_move(){

  // Decimos que empezamos el proceso
  serial_out(200);

  while (automatic){

    check_change_button();

    if (Serial.available() > 0) {

      String receivedString = Serial.readStringUntil('\n');
      StaticJsonDocument<200> jsonDoc;
      DeserializationError error = deserializeJson(jsonDoc, receivedString);
      
      if (!error) {
        int state = jsonDoc["state"];

        if (state == 400){ 
          automatic = false;
          break;
        } 
        // else: ended == 200
        int x_value = jsonDoc["x_value"];
        int y_value = jsonDoc["y_value"];

        //Serial.print("Received values: {x_value: ");
        //Serial.print(x_value);
        //Serial.print(", y_value: "); 
        //Serial.print(y_value);
        //Serial.println();

        int x_ang = map( x_value, -1, 1, 45, 180 );
        int y_ang = map( y_value, -1, 1, 140, 100 );

        // Movemos
        move(x_ang, y_ang);
        delay(2000);

        // Recolocamos poco a poco
        int step = 1;
        if (y_ang > central_internal_servo){
          step = -1;
        } 

        x_value = 0;
        y_value = 0; 
        x_ang = map( x_value, -1, 1, 45, 180 );

        y_ang = y_ang + step;
        while (y_ang != central_internal_servo){
          move(x_ang, y_ang);
          y_ang = y_ang + step;
          delay(200);
        }
        
        delay(500);

        // Decimos que continuamos
        serial_out(300);
      }
      else {

        //Serial.print("error");
      }

      

    }

  }

}


void manual_move(){
  // Posiciones del joystick
  int x = analogRead(PIN_VRx);
  int y = analogRead(PIN_VRy);
  // Mapeo de los valores a grados (0-180)

  int x_ang = map( x, 0, 1023, 45, 180 );

  int y_ang = map( y, 0, 512, 138, 119 );
  if (y > 512){
     y_ang = map( y, 512, 1023, 119, 110 );
  }

  
  //y_ang = 100; //120 centro; //140

  //Print de los valores en monitor serie
  
  /*
  Serial.print( "Joystick x value:" );
  Serial.print(x);
  Serial.print("  ");

  Serial.print( "Joystick y value:" );
  Serial.print(y);
  */
  
  //Desplazar servomotores
  move(x_ang, y_ang);
	
  // servoExterior.write(x_ang);
  // servoInterior.write(y_ang);

}



// Comprobamos si se ha pulsado el joystick
//
// Si se ha pulsado, cambiamos a modo automatico
void check_change_button(){

  int change = digitalRead(PIN_SW);

  // 0 pulsado -- 1 no pulsado
  /*
  Serial.print( " SW (Boton joystick):");
  Serial.print( change );
  Serial.println();
  */

  // Queremos cambiar
  if (change == 0){

    // Si estabamos en automatico, mandamos mensaje de cancelacion
    if (automatic){
      serial_out(400);
      digitalWrite(LED_BUILTIN, LOW); // Apagamos el LED

      /*
      Serial.print( "====================================");
      Serial.print( "Cancelando. Volviendo a modo manual.");
      Serial.print( "====================================");
      */
      automatic = false;
    }
    else{
      /*
      Serial.print( "============================");
      Serial.print( "Entrando a modo automatico.");
      Serial.print( "============================");
      */

      automatic = true;
    }

    //automatic = !automatic;


    delay(1000);
  }
}



/////////////////////////////////////
/////// FUNCIONES PRINCIPALES ///////
/////////////////////////////////////

// Inicializaciones
void setup(){
  
  // inicializar monitor serie a 9600 baudios
  Serial.begin(9600);
  analogReference(DEFAULT);

  //  Configuramos pin del pulsador del joystick como entrada con pullup
  pinMode(PIN_SW, INPUT_PULLUP);
  pinMode(PIN_VRx, INPUT); // Configurar el pin como entrada
  pinMode(PIN_VRx, INPUT); // Configurar el pin como entrada

  pinMode(LED_BUILTIN, OUTPUT);


	//Enlazamos el motor exterior al pin PIN_SERVO_EXT
	servoExterior.attach(PIN_SERVO_EXT);
  servoExterior.write(central_external_servo);

	//Enlazamos el motor interior al pin PIN_SERVO_INT
	servoInterior.attach(PIN_SERVO_INT);
  servoInterior.write(central_internal_servo);
}


// Bucle principal
void loop(){

  
  if (!automatic){
    //serial_out(200);
    //Serial.print( "manual");
    //Serial.println();
    manual_move();
  }
  else {

    automatic_move();

    //Serial.print( "=========================");
    //Serial.print( "Volviendo a modo manual.");
    //Serial.print( "=========================");

    //automatic = false;
    //serial_out(400);
    digitalWrite(LED_BUILTIN, HIGH); // Apagamos el LED
  }

  check_change_button();
  //Serial.print("Automatic= ");
  //Serial.print(automatic);
  //Serial.println();


  //Esperar 1/4 de segundo (en milisegundos)
	//delay(1000);
  

}
