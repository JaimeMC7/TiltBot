
import copy
import cv2
import numpy as np


img_folder = "images/"
img_name = "foto17"


#########################################################################
###### SEPARA UNA IMAGEN ORIGEN EN IMAGENES BINARAS SEGUN EL COLOR ######
#########################################################################
def separador_colores(original_img_path):
    # Leer la imagen
    image = cv2.imread(original_img_path)
    image = cv2.resize(image, (200, 200))


    # Convertir la imagen a espacio de color HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir rangos para el color azul
    lower_blue = np.array([90, 140, 40])
    upper_blue = np.array([140, 255, 255])

    # Definir rangos para el color rojo
    lower_red1 = np.array([0, 150, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 50])
    upper_red2 = np.array([180, 255, 255])

    # Definir rangos para el color verde
    lower_green = np.array([40, 150, 50])
    upper_green = np.array([80, 255, 255])

    # Definir rangos para el color negro
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])  # Valores bajos en el canal V

    # Crear una máscara para el color azul
    mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Crear una máscara para el color rojo (dos rangos por la naturaleza circular del color rojo en HSV)
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Crear una máscara para el color verde
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)

    # Crear una máscara para el color negro
    mask_black = cv2.inRange(hsv_image, lower_black, upper_black)

    # Guardar las imágenes resultantes
    cv2.imwrite(img_folder + 'blue_binary_img.png', mask_blue)
    cv2.imwrite(img_folder + 'red_binary_img.png', mask_red)
    cv2.imwrite(img_folder + 'green_binary_img.png', mask_green)
    cv2.imwrite(img_folder + 'black_binary_img.png', mask_black)


####################################################
###### ENCUENTRA EL PUNTO CENTRAL DE CIRCULOS ######
####################################################
def encontrar_y_marcar_centroide(imagen_path, output_path):
    # Leer la imagen en escala de grises
    image = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)

    # Binarizar la imagen (convertirla a blanco y negro)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Encontrar los contornos
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Verificar si se encontraron contornos
    if len(contours) > 0:
        # Tomar el primer contorno (puedes modificar esto si hay múltiples contornos)
        cnt = contours[0]

        # Calcular los momentos del contorno
        M = cv2.moments(cnt)

        # Calcular las coordenadas del centroide
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Calcular el área de la zona blanca
        area = M["m00"]

        # Calcular el radio del círculo equivalente
        radio = np.sqrt(area / np.pi)

        # Leer la imagen original en color para dibujar el punto negro
        color_image = cv2.imread(imagen_path)

        # Dibujar el punto negro en la imagen
        cv2.circle(color_image, (cX, cY), 1, (0, 0, 0), -1)

        # Guardar la imagen con el punto negro
        cv2.imwrite(output_path, color_image)

        # Devolver las coordenadas del centroide y el radio
        return cX, cY, radio
    else:
        return None, None, None



#######################################
###### ENGORDA LAS ZONAS BLANCAS ######
#######################################
def ensanchar_zona(imagen_path, output_path, grosor=10):
    # Leer la imagen en escala de grises
    binary_image = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    print("Ensanchar_zona, zona roja shape: ", binary_image.shape)

    # Aumentar el grosor de la zona usando dilatación
    if grosor > 1:
        kernel = np.ones((grosor, grosor), np.uint8)
        binary_image = cv2.dilate(binary_image, kernel, iterations=1)
        binary_image = cv2.erode(binary_image, kernel, iterations=1)

    # Guardar la imagen
    binary_image = cv2.resize(binary_image, (200, 200))
    cv2.imwrite(output_path, binary_image)

    # Devolver la imagen
    return binary_image



###################################################
###### FUNCION DONDE SE HACE Todo EL PROCESO ######
###################################################
def alg_paredes():
    ## Leemos la imagen original con los colores mezclados, y la separamos 
    ##  en diferentes imagenes, 1 imagen binaria por color.
    ## 
    ## Las imagenes finales son: (blue/red/green)_binary_img.png
    img_path = "img.png"

    separador_colores(img_path)
    
    ### Leemos las imagenes binarias de los colores y las reescalamos a 200x200 
    ##  (para reducir el futuro computo)
    b_img = cv2.imread(img_folder + 'blue_binary_img.png')
    b_gray_image = cv2.cvtColor(b_img, cv2.COLOR_BGR2GRAY)
    b_gray_image = cv2.resize(b_gray_image, (200, 200))
    cv2.imwrite(img_folder + 'b_gray_image.png', b_gray_image)

    r_img = cv2.imread(img_folder + 'red_binary_img.png')
    r_gray_image = cv2.cvtColor(r_img, cv2.COLOR_BGR2GRAY)
    r_gray_image = cv2.resize(r_gray_image, (200, 200))
    cv2.imwrite(img_folder + 'r_gray_image.png', r_gray_image)
    
    g_img = cv2.imread(img_folder + 'green_binary_img.png')
    g_gray_image = cv2.cvtColor(g_img, cv2.COLOR_BGR2GRAY)
    g_gray_image = cv2.resize(g_gray_image, (200, 200))
    cv2.imwrite(img_folder + 'g_gray_image.png', g_gray_image)
    
    """
    # Muestra de las imagenes binarias reescaladas 
    cv2.imshow('Imagen azul binaria nueva', b_gray_image)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    print(b_gray_image.shape)
    cv2.imshow('Imagen roja binaria nueva', r_gray_image)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    print(r_gray_image.shape)
    cv2.imshow('Imagen verde binaria nueva', g_gray_image)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    print(g_gray_image.shape)
    """
    


    ## Encontramos el centro de la bola (zona blanca de la imagen binaria azul)
    start_center_y, start_center_x, radio_bola = encontrar_y_marcar_centroide(img_folder + 'b_gray_image.png', img_folder + 'b_centroid.png')

    if start_center_x is not None and start_center_y is not None:
        print(f"El centroide de la zona azul está en: ({start_center_x}, {start_center_y})")
        print(f"Y tiene un radio de: ({radio_bola})")
    else:
        print("No se encontraron zonas blancas en la imagen.")
    
    ## Encontramos el centro de la zona destino (zona blanca de la imagen binaria verde)
    finish_center_y, finish_center_x, radio_final = encontrar_y_marcar_centroide(img_folder + 'g_gray_image.png', img_folder + 'g_centroid.png')

    if finish_center_x is not None and finish_center_y is not None:
        print(f"El centroide de la zona verde está en: ({finish_center_x}, {finish_center_y})")
        print(f"Y tiene un radio de: ({radio_final})")
    else:
        print("No se encontraron zonas blancas en la imagen.")
    

    ## Ensanchamos la zona blanca
    zona_ensanchada = ensanchar_zona(img_folder + 'r_gray_image.png', img_folder + 'red_zone.png', int(radio_bola))
    cv2.imwrite(img_folder + 'red_thick_zone.png', zona_ensanchada)


    ### Sumar "ciruclo de inicio" a la imagen binaria de las paredes
    #zona_ensanchada = zona_ensanchada + b_gray_image


    """
    # Muestra del perimetro encontrado de las zonas rojas
    cv2.imshow('Zona ensanchada', zona_ensanchada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """


    ##### NO SE UTILIZA, POR AHORA [UNUSED]
    #red_zone_contourns = extract_internal_contours(img_folder + "red_zone.png")
    #cv2.imwrite(img_folder + 'red_zone_contourns.png', red_zone_contourns)





    ## Encontrar esquinas 
    red_zone_corners = detect_corners(img_folder + "red_zone.png")
    cv2.imwrite(img_folder + 'red_zone_contourn_points.png', red_zone_corners)

    original_img = cv2.imread(img_path)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

    int_corners, ext_corners, closest_corner_start, closest_corner_end = identify_corners(zona_ensanchada, red_zone_corners, [start_center_x, start_center_y], [finish_center_x, finish_center_y])
    encontrar_camino_paredes(original_img, zona_ensanchada, int_corners, ext_corners, closest_corner_start, closest_corner_end, [start_center_x, start_center_y], [finish_center_x, finish_center_y], red_zone_corners)


##################
#### [UNUSED] ####
#####################################################################
###### DEVUELVE UNA IMAGEN CON LOS CONTORNOS DE LA ZONA BLANCA ######
#####################################################################
def extract_internal_contours(image_path):
    # Cargar la imagen en blanco y negro
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Asegurarse de que la imagen sea binaria
    _, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Encontrar contornos y jerarquía
    contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # Crear una imagen negra del mismo tamaño que la original
    contour_img = np.zeros_like(binary_img)

    # Dibujar los contornos internos en la imagen negra
    for i in range(len(contours)):
        if hierarchy[0][i][3] != -1:  # Si el contorno tiene un padre (no es externo)
            cv2.drawContours(contour_img, contours, i, (255), 1)

    # Aplicar dilatación a los contornos para unir los píxeles de las esquinas
    kernel = np.ones((3,3),np.uint8)
    contour_img = cv2.dilate(contour_img, kernel, iterations=1)

    return contour_img


#########################################################
###### CALCULA LA DISTANCIA ENTRE EL PUNTO p1 y p2 ######
#########################################################
def calc_dist_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


##########################################################################
###### ENCUENTRA EL PUNTO MAS CERCANO AL PUNTO p DE LA LISTA points ######
##########################################################################
def punto_mas_cercano(wall_img, points, p):
    closest_corner = [-1, -1]
    closest_dist = 99999

    for point in points:
        
        if wall_between(wall_img, point, p):
            continue

        dist = calc_dist_squared(point, p)

        if dist < closest_dist:
            closest_corner = [point[0], point[1]]
            closest_dist = dist
    
    return closest_corner


#####################################################################
###### PASA LOS PIXELES QUE SEAN == 255 A LISTA DE COORDENADAS ######
#####################################################################
def img_to_points(img):
    print("tamano imagen res:", img.shape)

    points = []

    for j in range(img.shape[0]):
        for i in range(img.shape[1]):

            if img[i][j] == 255:
                points.append([i, j])
    
    return points



############################################################
###### COMPROBAMOS QUE ESQUINA ES INTERNA O EXTERNA   ######
############################################################
def intern_and_extern_corners(wall_img, corners):

    int_corners = []
    ext_corners = []

    aux = 4
    for corner in corners:
        walls = [0, 0, 0, 0]

        for index, side in enumerate([[aux, aux], [aux, -aux], [-aux, aux], [-aux, -aux]]):
            
            x = corner[0] + side[0]
            x = min(x, wall_img.shape[0]-1)
            y = corner[1] + side[1]
            y = min(y, wall_img.shape[1]-1)

            if wall_img[x][y] == 255:
                walls[index] = 1

        if sum(walls) <= 2:
            int_corners.append(corner)
        else:
            ext_corners.append(corner)

    return int_corners, ext_corners




#######################################################
###### CALCULO DE LAS ESQUINAS MAS CERCASNAS A   ######
###### INICIO Y FINAL Y PASO DE PUNTOS DE IMG A  ######
######          LISTA DE COORDENADAS             ######
#######################################################
def identify_corners(wall_img, img_corners, coord_bola, coord_final):

    corner_points = img_to_points(img_corners)

    int_corners, ext_corners = intern_and_extern_corners(wall_img, corner_points)

    closest_corner_to_start = punto_mas_cercano(wall_img, ext_corners, coord_bola)
    closest_corner_to_end = punto_mas_cercano(wall_img, ext_corners, coord_final)


    print("Bola en: (", coord_bola[0], ", ", coord_bola[1], ")")
    print("Esquina mas cercana en: (", closest_corner_to_start[0], ", ", closest_corner_to_start[1], ")")

    print("Final en: (", coord_final[0], ", ", coord_final[1], ")")
    print("Esquina mas cercana en: (", closest_corner_to_end[0], ", ", closest_corner_to_end[1], ")")


    return int_corners, ext_corners, closest_corner_to_start, closest_corner_to_end



def wall_between(wall_img, punto1, punto2):
    p1 = copy.deepcopy(punto1[::-1])
    p2 = copy.deepcopy(punto2[::-1])


    low_x = p2[0]
    high_x = p1[0]

    low_y = p2[1]
    high_y = p1[1]

    if p1[0] < p2[0]:
        low_x = p1[0] 
        high_x = p2[0]


    if p1[1] < p2[1]:
        low_y = p1[1]
        high_y = p2[1] 
    
    # Dibujar la línea en una imagen auxiliar
    line_image = np.zeros_like(wall_img)
    cv2.line(line_image, p1, p2, 255, 1)

    # Verificar si hay algún valor igual a 255 en la línea dibujada
    result = sum(wall_img[line_image == 255]) > 2*255 

    if result:
        return True
    
    return False

def horizontal_or_vertical(punto1, punto2):
    p1 = copy.deepcopy(punto1[::-1])
    p2 = copy.deepcopy(punto2[::-1])

    tolerance = 10
    aligned_point = copy.deepcopy(punto2)

    if abs(p1[1] - p2[1]) < tolerance:
        aligned_point[0] = p1[1]
        return 'H', aligned_point, punto2
    elif abs(p1[0] - p2[0]) < tolerance:
        aligned_point[1] = p1[0]
        return 'V', aligned_point, punto2
    
    return 'D'





def dibujar_linea(image, punto1, punto2, color=(255, 255, 255), grosor=2):
    # Dibujar la línea en la imagen
    punto1 = punto1[::-1]
    punto2 = punto2[::-1]
    print("linea de p1:", punto1, " a p2:", punto2)
    imagen_con_linea = cv2.line(image, tuple(punto1), tuple(punto2), color, grosor)
    return imagen_con_linea


def first_wall_point(wall_img, line_start_p, line_next_p):
    print("******************************")
    print("Esquina interior. Buscando muro siguiente")
    print("******************************")

    print("Punto inicio: ", line_start_p, " punto int:", line_next_p)

    diff = [0, 0]
    diff[0] = line_next_p[0] - line_start_p[0]
    diff[1] = line_next_p[1] - line_start_p[1]

    axis = 0

    pos_x = line_next_p[0]
    pos_y = line_next_p[1]


    if diff[0] == 0:
        axis = 1

    desp = ( diff[axis]/abs(diff[axis]) )

    if axis == 0:
        pos_x = int(pos_x + desp)
    else:
        pos_y = int(pos_y + desp)

    while wall_img[pos_x,pos_y] != 255:
        if axis == 0:
            pos_x = int(pos_x + desp)
        else:
            pos_y = int(pos_y + desp)
    
    if axis == 0:
        pos_x = int(pos_x - desp)
    else:
        pos_y = int(pos_y - desp)

    return [pos_x, pos_y]


def clean_path(path):

    prev_point = path[0]
    index_to_remove = []
    
    deleted = False

    for index in range(1, len(path) - 1):
        act_point = path[index]
        next_point = path[index + 1]

        deleted = False

        repeated_axis = 0
        repeated_val = act_point[0]

        tolerance = 5

        if abs(act_point[1] - prev_point[1]) < tolerance:
            repeated_axis = 1
            repeated_val = act_point[1]
        
        if act_point == [77, 19]:
            print("aqui?")

        if abs(next_point[repeated_axis] - repeated_val) < tolerance:
            index_to_remove.append(index)
        else:
            prev_point = act_point
    
    cleaned_path = []

    for index, point in enumerate(path):
        if index in index_to_remove:
            continue

        cleaned_path.append(point)
    
    return cleaned_path


            

        


        







#############################################################
###### ALGORITMO DE BUSQUEDA DEL CAMINO HASTA EL FINAL ######
#############################################################
def encontrar_camino_paredes(original_img, wall_img, int_corners, ext_corners, closest_corner_start, closest_corner_end, coord_bola, coord_final, red_zone_corners):
    ## Encontra camino entre puntos (mirar lineas rectas slo hast aencontrar un punto en una direccion)
    ## "Guardar" que inclinacion teniamos (par saber dondeestan las paredes, y como deberia estan mantenida 
    ##  la inclinacion en el lab)
    grosor = 8
    kernel = np.ones((grosor, grosor), np.uint8)
    unthik_wall_img = cv2.erode(wall_img, kernel, iterations=1)
    cv2.imwrite(img_folder + 'red_zone_unthikened.png', unthik_wall_img)

    """
    # Muestra del perimetro encontrado de las zonas rojas
    cv2.imshow('Zona des ensanchada', unthik_wall_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """


    corners = int_corners + ext_corners

    
    act_corner = closest_corner_start
    path = []
    used_corners = [closest_corner_start]
    next_corner = act_corner
    
    
    real_arrived_corner = act_corner

    count = 0
    while real_arrived_corner != closest_corner_end and count < 100:
        print("=====================")
        dist_to_end = 99999 

        associated_aproximations = []
        next_corner = [-1, -1]

        for corner in corners:

            res = horizontal_or_vertical(act_corner, corner) 

            if res[0] == 'D':
                continue

            aligned_corner, real_corner = res[1], res[2]
            associated_aproximations.append([aligned_corner, real_corner])
           
            if aligned_corner == [184, 181]:
                print("aqui")


            if corner == act_corner or wall_between(unthik_wall_img, act_corner, aligned_corner):
                continue

            

            if real_corner in used_corners:
                continue

            dist = calc_dist_squared(aligned_corner, closest_corner_end)

            if dist < dist_to_end:
                dist_to_end = dist
                next_corner = aligned_corner
            else:
                continue
        
        for aproximation in associated_aproximations:
            if aproximation[0] == next_corner:
                used_corners.append(aproximation[1])
                real_arrived_corner = aproximation[1]

                #print("Aprox:", aproximation)
        
        if next_corner == [-1, -1]:
            print("Sin camino. Vuelta atras.")
            if len(path) == 1:
                print("No hay solucion")
                exit(1)

            path = path[:-1]
            act_corner = path[-1]
        else:
            print("Camino. Adelante")                
            
            

            if real_arrived_corner in int_corners:
                next_corner = first_wall_point(wall_img, act_corner, next_corner)
                real_arrived_corner = next_corner
                print("First wall point: ", next_corner)
                
            path.append(next_corner)
            
            act_corner = next_corner

        count += 1
        print("Count = ", count)
        print("Path: ", path)
    
    print("path sin limpiar:", path)

    prev_path = []
    cleaned_path = copy.deepcopy(path)

    while cleaned_path != prev_path:
        prev_path = copy.deepcopy(cleaned_path)
        cleaned_path = clean_path(prev_path)


    print("path limpio:", cleaned_path)
    #path.append(closest_corner_end)
    
    not_cleaned_path_img = copy.deepcopy(red_zone_corners)
    cleaned_path_img = copy.deepcopy(red_zone_corners)

    # Dibujar la línea en la imagen
    act_point = closest_corner_start
    for point in path:
        not_cleaned_path_img = dibujar_linea(not_cleaned_path_img, act_point, point)
        act_point = point
    
    # Dibujar la línea en la imagen
    act_point = closest_corner_start
    for point in cleaned_path:
        cleaned_path_img = dibujar_linea(cleaned_path_img, act_point, point)
        act_point = point

    # Dibujar la línea en la imagen
    act_point = closest_corner_start
    for point in cleaned_path:
        original_img = dibujar_linea(original_img, act_point, point)
        act_point = point

    
    
##############################################################
#### Funciones para intentar quitar reflejos (no van aun) ####
##############################################################
def smallest_bounding_square(image):
    # Convertir la imagen a escala de grises si es necesario
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Binarizar la imagen
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Encontrar los límites superior, inferior, izquierdo y derecho de las áreas blancas
    coords = np.column_stack(np.where(thresh > 0))
    top_left = np.min(coords, axis=0)
    bottom_right = np.max(coords, axis=0)

    # Calcular las coordenadas del cuadrado de menor tamaño
    x, y = top_left
    w, h = bottom_right - top_left

    return (x, y, w, h)


def detect_white_except_in_roi(image, x, y, w, h):
    # Convertir la imagen a escala de grises si es necesario
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Mostrar la imagen con el rectángulo dibujado
    cv2.imshow('Img gris ', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Binarizar la imagen para obtener solo el color blanco
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    print("thresh:", thresh)

    # Crear una máscara para el área de interés (ROI)
    mask_roi = np.zeros_like(thresh)
    mask_roi[y:y+h, x:x+w] = 255

    # Aplicar la máscara inversa para excluir el área de interés
    mask = cv2.bitwise_not(mask_roi)

    # Aplicar la máscara para obtener solo el color blanco fuera del área de interés
    white_except_in_roi = cv2.bitwise_and(thresh, thresh, mask=mask)

    return white_except_in_roi

##############################################################


##################################################
###### ENCUENTRA LAS ESQUINAS DEL LABERINTO ######
##################################################
def detect_corners(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    # Detectar las esquinas usando el detector de esquinas Harris
    gray = np.float32(img)
    dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)

    # Aplicar un umbral para binarizar la imagen (por ejemplo, umbral de 127)
    _, dst_bin = cv2.threshold(dst, 0.01 * dst.max(), 255, cv2.THRESH_BINARY)

    # Encontrar contornos de las esquinas binarizadas
    contours, _ = cv2.findContours(dst_bin.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear una nueva imagen para dibujar los puntos
    img_with_points = np.zeros_like(img)

    # Dibujar puntos en la nueva imagen
    for contour in contours:
        # Calcular el centroide del contorno
        M = cv2.moments(contour)
        if M['m00'] != 0:  # Verificar que el área no sea cero
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Dibujar un punto central en la nueva imagen
            cv2.circle(img_with_points, (cx, cy), 0, (255, 255, 255), -1)


    return img_with_points

def main():
    
    ### Leemos las imagenes binarias de los colores y las reescalamos a 200x200 
    ##  (para reducir el futuro computo)
    img_path = 'images/origin/' + img_name + '.jpg'

    img = cv2.imread(img_path)
    img = cv2.resize(img, (200, 200))
    cv2.imwrite('img.png', img)
    

    alg_paredes()


    






if __name__ == "__main__":
    main()