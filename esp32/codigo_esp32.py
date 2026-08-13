import machine
from machine import Pin
import network
import time
import camera
from time import sleep
from mqttsimple import MQTTClient
import random

# --- CONEXIÓN WI-FI ---
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print("Conectando a la red...")
    sta_if.active(True)
    sta_if.connect("LaSalleWifi", "")
    while not sta_if.isconnected():
        time.sleep(1)
        print("Esperando Conexión...")

print("✅ Wi-Fi Conectado. IP:", sta_if.ifconfig()[0])

# --- CONEXIÓN MQTT ---
broker = "test.mosquitto.org"
port = 1883
client_id = f'esp32-rubik-{random.randint(0, 1000)}'
client = MQTTClient(client_id=client_id, server=broker, port=port)
client.connect()
print("✅ Conectado a MQTT Broker")

TOPIC_IMAGE = "cam/esp32/image"
TOPIC_COMMAND = "cam/esp32/command"

def on_message(topico, msg):
    print("Comando recibido:", msg)
    if msg == b'CAPTURE':
        print("📸 ¡Iniciando secuencia de 6 fotos para el cubo!")
        foto = 1
        
        while foto <= 6:
            nombre = f"Cap{foto}.jpg"
            print(f"\n--- Tomando foto de la CARA {foto} ---")
            
            try:
                # Inicializar cámara
                camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
                camera.framesize(camera.FRAME_XGA)
                camera.quality(10)
                
                # Capturar
                img = camera.capture()
                print(f"Tamaño capturado: {len(img)} bytes")
                camera.deinit()
                
                # Guardar en memoria local (opcional)
                with open(nombre, "wb") as imgFile:
                    imgFile.write(img)
                
                # --- TRANSMITIR POR MQTT ---
                print(f"📡 Enviando cara {foto} por MQTT...")
                # Enviar etiqueta de inicio con el número de cara (Ej: START_1)
                client.publish(TOPIC_IMAGE, f"START_{foto}".encode())
                time.sleep(0.1)

                CHUNK = 1024
                for i in range(0, len(img), CHUNK):
                    client.publish(TOPIC_IMAGE, img[i:i+CHUNK])
                    time.sleep(0.01)

                # Enviar etiqueta de fin con el número de cara (Ej: END_1)
                client.publish(TOPIC_IMAGE, f"END_{foto}".encode())
                print(f"✅ Cara {foto} enviada con éxito.")
                
                foto += 1
                
                if foto <= 6:
                    print("👉 ¡MUEVE EL CUBO A LA SIGUIENTE CARA!")
                    print("Tienes 8 segundos...")
                    sleep(8) # Tiempo para que gires el cubo
                
            except Exception as err:
                print("❌ Error en cámara/envío:", str(err))
                sleep(2)
                
        print("\n🎉 ¡Las 6 caras han sido capturadas y enviadas!")

client.set_callback(on_message)        
client.subscribe(TOPIC_COMMAND)

print("⏳ Esperando comando 'CAPTURE' desde Flask...")
while True:
    client.check_msg()
    time.sleep(0.5)
