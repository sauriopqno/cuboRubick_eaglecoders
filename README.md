# Solucionador de Cubo mediante BFS 🧊

Este repositorio contiene un script en Python que resuelve un rompecabezas de cubo 
(con 24 posiciones, equivalente a un cubo de Rubik 2x2) utilizando el algoritmo de *Búsqueda en Anchura (BFS)*. 
El programa encuentra la ruta más corta (la menor cantidad de movimientos) desde un estado inicial desordenado 
hasta el estado resuelto.

## ¿Cómo funciona?

El cubo se representa mediante una lista de 24 números, donde cada número corresponde a una etiqueta o color en específico. 
El estado final se verifica comprobando que cada cara del cubo contenga los números correctos agrupados.

El algoritmo explora el árbol de posibles movimientos utilizando una estructura de datos de cola (deque de la librería collections). 
Al usar BFS, el programa garantiza encontrar la solución óptima.

### Movimientos permitidos

El script simula las rotaciones de las caras del cubo basándose en la notación clásica de los cubos de Rubik:
*   U (Up) - Rotación de la cara superior en sentido horario.
*   U' (Up anti) - Rotación de la cara superior en sentido antihorario.
*   F (Front) - Rotación de la cara frontal en sentido horario.
*   F' (Front anti) - Rotación de la cara frontal en sentido antihorario.
*   R (Right) - Rotación de la cara derecha en sentido horario.
*   R' (Right anti) - Rotación de la cara derecha en sentido antihorario.

## Requisitos previos

Para ejecutar este código, necesitas tener Python instalado en tu sistema operativo. 
No se requieren librerías externas de terceros, ya que utiliza la librería estándar de Python.
