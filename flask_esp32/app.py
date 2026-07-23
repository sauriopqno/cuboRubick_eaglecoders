from flask import Flask, send_file, render_template, request
import paho.mqtt.client as mqtt
import threading
import os

app = Flask(__name__)

MQTT_BROKER = "test.mosquitto.org"
TOPIC_COMMAND = "cam/esp32/command"
TOPIC_IMAGE = "cam/esp32/image"

image_buffer = bytearray()
current_face = None  # Variable para saber qué cara se está recibiendo

def on_connect(client, userdata, flags, rc):
    print("✅ Servidor Flask conectado a MQTT")
    client.subscribe(TOPIC_IMAGE)

def on_message(client, userdata, msg):
    global image_buffer, current_face

    payload = msg.payload

    # Verificar si es el inicio de una cara (Ej: b"START_1")
    if payload.startswith(b"START_"):
        current_face = payload.decode().split("_")[1] # Extrae el número
        image_buffer = bytearray()
        print(f"\n🟢 Recibiendo imagen de la CARA {current_face}...")

    # Verificar si es el fin de la cara (Ej: b"END_1")
    elif payload.startswith(b"END_"):
        if current_face:
            os.makedirs("static", exist_ok=True)
            filepath = f"static/photo_{current_face}.jpg"
            
            with open(filepath, "wb") as f:
                f.write(image_buffer)
                
            print(f"💾 CARA {current_face} guardada en '{filepath}' ({len(image_buffer)} bytes)")
            
            if int(current_face) < 6:
                print("👉 ¡Mueve el cubo a la siguiente cara!")
            else:
                print("🏁 ¡LAS 6 CARAS COMPLETADAS! Listo para resolver.")
                
            current_face = None

    # Si no es START ni END, son los bytes de la imagen
    else:
        if current_face is not None:
            image_buffer.extend(payload)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)

def mqtt_loop():
    mqtt_client.loop_forever()

threading.Thread(target=mqtt_loop, daemon=True).start()

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/capture")
def capture():
    print("🚀 Enviando comando de captura al ESP32...")
    mqtt_client.publish(TOPIC_COMMAND, "CAPTURE")
    return """
    <h1>Comando CAPTURE enviado al ESP32</h1>
    <p>Tienes 8 segundos entre cada foto para girar el cubo.</p>
    <h3>Ver fotos capturadas:</h3>
    <ul>
        <li><a href="/photo/1" target="_blank">Cara 1</a></li>
        <li><a href="/photo/2" target="_blank">Cara 2</a></li>
        <li><a href="/photo/3" target="_blank">Cara 3</a></li>
        <li><a href="/photo/4" target="_blank">Cara 4</a></li>
        <li><a href="/photo/5" target="_blank">Cara 5</a></li>
        <li><a href="/photo/6" target="_blank">Cara 6</a></li>
    </ul>
    <br><a href="/">Volver</a>
    """

# Ahora puedes pedir el número de cara en la URL: ejemplo /photo/1 o /photo/6
@app.route("/photo/<int:face_id>")
def photo(face_id):
    filepath = f"static/photo_{face_id}.jpg"
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="image/jpeg")
    return f"❌ No se ha recibido la imagen de la cara {face_id} aún."

@app.route("/solution")
def solution():
    return "<h1>Aquí irá el algoritmo para resolver el cubo</h1>"

if __name__ == "__main__":
    app.run(debug=True)