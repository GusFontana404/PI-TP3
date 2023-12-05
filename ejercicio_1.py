# --- Función para contar el número de los dados --------------------------------------------------------------------------
def contar_huecos(imagen):

  #Encontrar contornos internos
  contornos, jerarquia = cv2.findContours(imagen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

  #Contar los contornos encontrados
  contornos_internos = sum(1 for h in jerarquia[0] if h[3] != -1)
  
  return contornos_internos


# --- Función para procesar los frames y obtener los dados -----------------------------------------------------------------
def encontrar_dados(frame):
    #Convertir la imagen de BGR a HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Definir el rango de colores rojos en HSV
    rango_bajo = np.array([0, 75, 75])   
    rango_alto = np.array([5, 255, 255])  

    #Crear una máscara utilizando inRange para la segmentación
    mascara1 = cv2.inRange(img_hsv, rango_bajo, rango_alto)

    #Definir otro rango de colores rojos en HSV 
    rango_bajo = np.array([90, 75, 75])  
    rango_alto = np.array([180, 255, 255]) 

    #Crear otra máscara utilizando inRange para la segmentación
    mascara2 = cv2.inRange(img_hsv, rango_bajo, rango_alto)

    #Combinar ambas máscaras para incluir ambos rangos de rojo
    mascara_roja = cv2.bitwise_or(mascara1, mascara2)

    #Aplicar la máscara a la imagen original
    img_segmentada = cv2.bitwise_and(frame, frame, mask=mascara_roja)

    #Pasar imagen a gris
    img_gray = cv2.cvtColor(img_segmentada, cv2.COLOR_BGR2GRAY)

    #Binarizar la imagen
    th, binary_img = cv2.threshold(img_gray, 28, 1, cv2.THRESH_BINARY) 

    #Morfología para mejorar la segmentación obtenida
    morf_ap = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 2)) 
    morf_cl = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1)) 

    #Apertura para remover elementos pequeños
    imagen_apertura = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, morf_ap)

    #Clausura para rellenar huecos.
    clausura_img = cv2.morphologyEx(imagen_apertura, cv2.MORPH_CLOSE, morf_cl)
    
    return clausura_img

# --- Funcion para leer un video y generar la detección de dados -------------------------------------------------------------
def video_segmentado(video):
    cap = cv2.VideoCapture(video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    #Video de salida
    out = cv2.VideoWriter(f'{video}-Output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width/3),int(height/3)))
    
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            #Procesamiento
            frame_original = cv2.resize(frame, dsize=(int(width/3), int(height/3)))

            #Convertir el frame a escala de grises
            gray_frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)
            
            #Aplicar umbral al frame
            _, binary_mask = cv2.threshold(gray_frame, 75, 255, cv2.THRESH_BINARY)

            #Contar píxeles blancos
            píxeles_blancos = cv2.countNonZero(binary_mask)

            #Contar píxeles negros (total de píxeles - píxeles blancos)
            total_píxeles = binary_mask.size
            píxeles_negros = total_píxeles - píxeles_blancos

            #Resultados de la segmentación de la función
            #frame_procesado = encontrar_dados(frame_original) * 255
            #out.write(cv2.cvtColor(frame_procesado, cv2.COLOR_GRAY2BGR))

            #Detecta cambio de intensidad con respecto a una 'imagen estática'
            if píxeles_negros > 9500 and píxeles_negros < 14600:
                copia_frame = frame_original.copy()
                dados_staticos = encontrar_dados(copia_frame)

                #Buscar componentes conectadas
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dados_staticos)

                #Itera sobra las stats y filtra áreas (detectadas experimentalmente)
                for st in stats:
                    if st[4] > 300 and st[4] < 600:

                        #Encuentra las coordenadas del dado
                        x, y, ancho, alto = st[0]-5,st[1]-5,st[2]+10,st[3]+10
                            
                        #Extrae la ROI usando las coordenadas del dado
                        roi = dados_staticos[y:y+alto, x:x+ancho]  

                        #Cuenta los huecos internos del dado
                        nro_huecos = contar_huecos(roi)

                        #Traza el rectángulo sobre las coord de la ROI y coloca etiqutas con el nro del dado 
                        cv2.rectangle(copia_frame,(x,y),(x+ancho,y+alto),color=(255,0,0),thickness=2)
                        cv2.putText(copia_frame, f'{nro_huecos}', (st[0]+22, st[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
            else:
                copia_frame = frame_original
            
            #Guardar el frame modificado en el video de salida
            out.write(copia_frame)
            
            #Mostrar el cuadro original y la máscara de primer plano
            cv2.imshow('Frame Original', frame_original)
            #cv2.imshow('Mascara Binaria', binary_mask)

            #Mostrar el video segmentado
            #cv2.imshow('Frame Procesado', frame_procesado)

            #Mostar el video con la detección de dados
            cv2.imshow('Deteccion Dados', copia_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

