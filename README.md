## Procesamiento de Imágenes 

## Trabajo Práctico 3

## Integrantes:
- Fontana, Gustavo
- Brizuela Cipolletti, Sofía

## Consigna
El trabajo práctico consiste en:
- `Ejercicio 1` : Desarrollo de un algoritmo para detección automática de dados estáticos, que además, lee el número obtenido en cada uno. Se genera también videos (uno para cada archivo) cuando los dados están en reposo, resaltandos con un bounding box de color azul y una etiqueta sobre los mismos el número reconocido.

El script 'ejercicio_1.py' incluye tres funciones:
- `contar_huecos` : Detecta la cantidad de contornos internos en los dados y devuelve el valor representado en su cara superior.
- `encontrar_dados` : Recibe un video de tirada de dados y los procesa de tal manera que se obtienen los dados semgentados sobre el fondo.
- `video_segmentado` : Reproduce los videos de tiradas de dados y detecta cuando el fondo queda estático. Además, realiza la detección de dados y cuenta los valores que representan cada uno de ellos (llamando a las dos funciones anteriores), el resultado se refleja en el video mostrado en pantalla.
La ejecución de está función devuelve un video grabado con la segmentación incluidad en el.

## Archivos
- `Video Tiradas de Dados` : Carpeta donde se encuentran los videos para la detección del algoritmo 'ejercicio1.py'
- `ejercicio1.py` : Código Python del ejercicio 1

## Indicaciones
Para ejecutar el código, debe asegurarse que cuenta con `Python` instalado y con las siguientes librerías en el entorno de trabajo: 
- matplotlib.pyplot 
- numpy
- cv2 
