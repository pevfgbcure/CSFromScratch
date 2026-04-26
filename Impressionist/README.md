# Impressionist

## ¿Qué es?

Impressionist implementa un algoritmo estocástico para generar una imagen a partir de otra, utilizando figuras simples como líneas, elipses, triángulos o cuadriláteros. El algoritmo se basa en la idea de que una imagen puede ser representada por una colección de figuras simples, y que al ajustar estas figuras para que se parezcan a la imagen original, se puede crear una representación artística de la misma.

## ¿Cómo funciona?

El algoritmo de Impressionist sigue los siguientes pasos:

1. Crea una imagen en blanco del mismo tamaño que la imagen original y la inicializa con un color de fondo que es el promedio de los colores de la imagen original.
2. Intenta dibujar la forma especificada (línea, elipse, triángulo o cuadrilátero) en la imagen en blanco, con un tamaño y posición aleatorios, y con un color que pueder ser el promedio de los colores de la imagen original, el color más común en la imagen original o un color aleatorio.
3. Compara los colores de la imagen generada con los colores de la imagen original. Si la forma dibujada mejora la similitud entre la imagen generada y la imagen original, se mantiene; de lo contrario, se descarta.
4. Intenta modificar las coordenadas de la forma seleccionada, añadiendo o restando un pixel a cada coordenada, moviendo la coordenada para reducir la diferencia entre la imagen generada y la imagen original. Cuando mover la coordenada no mejora la similitud, se mantiene la forma en su posición actual.
5. Repite los pasos 2 a 4 durante un número determinado de iteraciones (trials).
6. Devuelve la imagen generada.

## Uso

Tu sistema debe tener Python instalado, así como Pillow para el procesamiento de imágenes.

Para ejecutar el programa, se deben proporcionar al menos dos argumentos: la ruta de la imagen original y la ruta donde se guardará la imagen generada. Además, se pueden especificar otros argumentos opcionales, los cuales se describen a continuación:

| Opción            | Descripción                                                                                                                                                     | Posible valor                                  | Valor por defecto |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ----------------- |
| `-t`, `--trials`  | Número de iteraciones para el algoritmo. Cuanto más alto, mejor calidad de la imagen producida, pero más lento.                                                 | Entero positivo                                | 10000             |
| `-s`, `--shape`   | Tipo de forma a utilizar para generar la imagen.                                                                                                                | `line`, `ellipse`, `triangle`, `quadrilateral` | `ellipse`         |
| `-m`, `--method`  | Método para seleccionar el color de la forma.                                                                                                                   | `average`, `common`, `random`                  | `average`         |
| `-l`, `--length`  | El largo que tendrá la imagen generada.                                                                                                                         | Entero positivo                                | 256               |
| `-v`, `--vector`  | Si se especifica, también se generará una imagen vectorial en formato SVG.                                                                                      | Ninguno                                        | Ninguno           |
| `-a`, `--animate` | Si se proporciona un número mayor a 0, se generará un GIF animado que muestra el proceso de generación de la imagen, con un retraso entre cuadros especificado. | Entero positivo                                | 0                 |

### Ejemplo de uso

```powershell
python -m Impressionist [ruta_imagen_original] [ruta_imagen_generada] -t 100000 -s triangle -m common -l 512 -v -a 5
```

Este comando generará una imagen a partir de la imagen original, realizando 100,000 iteraciones, utilizando triángulos, seleccionando el color más común en la imagen original para cada triángulo, con un largo de 512 píxeles, y también generará una imagen vectorial en formato SVG y un GIF animado que muestra el proceso de generación de la imagen con un retraso de 5 milisegundos entre cuadros.
