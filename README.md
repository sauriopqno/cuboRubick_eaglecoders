
# cuboRubick_eaglecoders
> **Reporte de Avances y Documentación Técnica de Proyecto**  
> **Equipo:** EagleCoders 

---

## Resumen
El proyecto **cuboRubick_eaglecoders** es un sistema IoT distribuido diseñado para la captura, procesamiento y resolución automatizada de un **Cubo de Rubik (2x2)**. 

Combina captura de imágenes mediante un embebido **ESP32-CAM**, transmisión de baja latencia por eventos en un servidor **Flask**, y un motor algorítmico de inteligencia artificial basado en **Búsqueda en Anchura (BFS)** para calcular la secuencia óptima de movimientos.

---

## ¿Cómo Funciona el Sistema? (Capa por Capa)

```text
  [ 1. ESP32-CAM ]                  [ 2. SERVIDOR FLASK ]                 [ 3. MOTOR ALGORÍTMICO ]
┌─────────────────────────┐       ┌────────────────────────────┐        ┌────────────────────────────┐
│ • Captura las 6 caras.  │ ────► │ • Recibe y ensambla bytes. │ ─────► │ • Mapea estado inicial.    │
│ • Envía por fragmentos  │ MQTT  │ • Guarda photo_1 a photo_6.│ HTTP/  │ • Ejecuta búsqueda BFS.    │
│   (chunks de 1024 bytes)│       │ • Expone panel en Web UI.  │ Python │ • Retorna ruta óptima.     │
└─────────────────────────┘       └────────────────────────────┘        └────────────────────────────┘
```
1. Dispositivo Embebido (ESP32-CAM)
 * Captura con Buffering: La cámara captura la imagen en memoria PSRAM a resolución XGA (FRAME_XGA) para asegurar alta fidelidad.
 * Transmisión por Chunks vía MQTT: Para no colapsar la memoria del microcontrolador ni superar los límites del Broker MQTT, la imagen se segmenta en bloques de 1024 bytes.
 * Protocolo de Sincronización: Cada cara envía banderas de control (START_1 a START_6 y END_1 a END_6). Entre cara y cara, la ESP32 implementa un tiempo de espera automático de 8 segundos para permitir el giro físico del cubo.
2. Servidor Backend y Panel de Control (Flask)
 * Recepción Multihilo: Mantiene una conexión persistente escuchando los tópicos MQTT (cam/esp32/image).
 * Reconstrucción Dinámica de Archivos: A medida que llegan los fragmentos de datos, el servidor los acumula en un bytearray y los escribe en disco como photo_1.jpg ... photo_6.jpg dentro de la carpeta static/.
 * Interfaz Dashboard (Bootstrap 5): Permite disparar el evento de captura vía botón web (/capture) y visualizar las fotos actualizadas en tiempo real.
3. Algoritmo de Resolución (Búsqueda en Anchura - BFS)
 * Representación del Estado: El cubo de Rubik 2x2 se modela como una lista de 24 posiciones (4 posiciones por cada una de las 6 caras).
 * Matriz de Permutaciones de Movimiento: Se mapean los giros tridimensionales del cubo (U, F, R, U', F', R') como transposiciones numéricas de índices dentro del arreglo.
 * Exploración de Estados (BFS): Utiliza una cola doblemente terminada (collections.deque) para realizar una búsqueda en anchura sobre el árbol de estados posibles. Esto garantiza encontrar matemáticamente la secuencia con el menor número de movimientos posibles.
 * Criterio de Parada y Backtracking: Un método de validación (verificarFinal) revisa si cada cara contiene los 4 valores correlativos correctos. Una vez hallado el estado meta, se reconstruye la solución recorriendo la estructura de padres hacia atrás.
```text
Arquitectura del Repositorio
cuboRubick_eaglecoders/
├── esp32/                  # Firmware en MicroPython
│   ├── codigo_esp32.py     # Manejo de cámara, timers de 8s y cliente MQTT
│   └── mqttsimple.py       # Driver MQTT ligero para microcontroladores
├── esp32_fake/             # Emulador / Mock
│   └── fake_esp32cam.py    # Simulador de envío de imágenes para desarrollo en PC
├── flask_esp32/            # Backend y Algoritmos de Resolución
│   ├── static/             # Almacenamiento local de las 6 fotos recibidas
│   ├── templates/          # Interfaz web (main.html)
│   ├── app.py              # Servidor web, integración MQTT y ejecutor del algoritmo
│   └── requirements.txt    # Librerías necesarias (Flask, paho-mqtt)
└── .gitignore              # Control de versiones
```
Estado de Avance del Proyecto
| Módulo / Fase | Estado | Descripción Técnica |
|---|---|---|
| Transmisión IoT (MQTT) | 🟢 100% | Envío y reconstrucción de imágenes por fragmentos funcional. |
| Interfaz Web (Flask) | 🟢 100% | Panel responsivo listo con Bootstrap 5 para comando y previsualización. |
| Algoritmo de Resolución (BFS) | 🟢 100% | Lógica de grafos y permutaciones matriciales probada y funcional en Python. |
| Simulación de Hardware (Mocking) | 🟢 100% | Módulo esp32_fake listo para pruebas continuas sin dependencia de hardware. |
| Mapeo Visión por Computadora | 🟡 En Desarrollo | Integración entre la lectura de imágenes (photo_1..6.jpg) y el vector de entrada del algoritmo BFS. |
| creación del hardware (robot físico)| 🔴 No empezado | construcción de un robot autonomo para solucionar el cubo sin intervención. |

