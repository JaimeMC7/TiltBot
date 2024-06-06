import serial #pip install pyserial
import json
import sys

import subprocess

import vision as v


ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_7563031393635160B231-if00', 9600, timeout=1)


def send_data(state, x, y):
    data = {"state": state, "x_value": x, "y_value": y}
    json_data = json.dumps(data)
    ser.write((json_data + '\n').encode('utf-8'))  # Asegúrate de enviar un salto de línea


def calc_direction(p1, p2):
    y = -1
    if p1[0] > p2[0]:
      y = 1
    elif p1[0] == p2[0]:
      y = 0
    
    x = -1
    if p1[1] > p2[1]:
       x = 1
    elif p1[1] == p2[1]:
       x = 0
       
    return x, y 


def send_error():
    error_msg = [[-1,-1], [-1, 1], [1,1], [1,-1]]
    
    
    act_point = error_msg[0]
    send_data(200, act_point[0], act_point[1])
    
    index = 1
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("latin1").rstrip()
            print(line)

            try:
                #jsonObj = json.loads(line)
                pot = line
                print("value: ", pot)

                if pot == "300":
                    act_point = error_msg[index]
                    send_data(200, act_point[0], act_point[1])
                    
                    index += 1
                    
                    if index >= len(error_msg):
                      send_data(400, -1, -1)
                      break
                
                elif pot == "400": #fin
                    break
                

                ser.reset_input_buffer()
            except:
                print("Error")


def laberinth_algorithm():
    command = ["rpicam-jpeg", "-o", "/home/sergio/Vision_module/imagenes/originales/prueba.jpg", "-n"]
    try:
        subprocess.run(command, check=True)
        print("Imagen capturada exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"Error al capturar la imagen: {e}")
    
    # Calcular el cami del laberint
    print("entro")
    path = v.main()
    print(path)
    
    # Si no se ha encontrado un camino, damos una vuelta
    if len(path) == 0:
        send_error()
        return
        

    act_point = path[0]
    next_point = path[1]
    
    
    x, y = calc_direction(act_point, next_point)
    send_data(200, x, y)
    
    act_point = next_point
    
    index = 2
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("latin1").rstrip()
            print(line)

            try:
                #jsonObj = json.loads(line)
                pot = line
                print("value: ", pot)

                if pot == "300":
                    next_point = path[index]
                    x, y = calc_direction(act_point, next_point)
                    send_data(200, x, y)
                    
                    act_point = next_point
                    index += 1
                    
                    if index >= len(path):
                      send_data(400, -1, -1)
                      break
                
                elif pot == "400": #fin
                    break
                

                ser.reset_input_buffer()
            except:
                print("Error")
    
        
        
        





def main():


    
    # Espera de una señal en serie
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("latin1").rstrip()
            print(line)

            try:
                #jsonObj = json.loads(line)
                pot = line
                print("value: ", pot)

                if pot == "200":
                    laberinth_algorithm()
                    print("Valor: ", pot)
                elif pot == "400": #fin
                    print("valor: ", pot)
                

                ser.reset_input_buffer()
            except:
                print("Errorrr")
    




if __name__ == "__main__":
    main()