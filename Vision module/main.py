import serial #pip install pyserial
import json
import sys

import vision as v


def laberinth_algorithm():
    # Calcular el cami del laberint
    path = v.main()
    print(path)

    start_point = path[0]
    finish_point = path[-1]


    for point in path[1:]:
        
        
        x_direction = 0
        y_direction = 0
        

        if point[0] < start_point[0]:
            x_direction = -1
        elif point[0] > start_point[0]:
            x_direction = 1
        
        if point[1] < start_point[1]:
            y_direction = -1
        elif point[1] > start_point[1]:
            y_direction = 1
        




    #


def main():

    #ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    laberinth_algorithm()

    """
    # Espera de una señal en serie
    while False:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

            try:
                jsonObj = json.loads(line)
                pot = jsonObj.get('value')
                print("value: ", pot)

                if pot == 10:
                    laberinth_algorithm()

                

                ser.reset_input_buffer()
            except:
                print("Error")
    """




if __name__ == "__main__":
    main()