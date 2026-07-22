from flask import Flask, send_file, render_template, request, redirect, url_for
import paho.mqtt.client as mqtt
import threading
import os

app = Flask(__name__)

IMAGE_PATH = "static/photo.jpg"
MQTT_BROKER = "test.mosquitto.org"
TOPIC_COMMAND = "cam/esp32/command"
TOPIC_IMAGE = "cam/esp32/image"

image_buffer = bytearray()

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado a MQTT")
    client.subscribe(TOPIC_IMAGE)

def on_message(client, userdata, msg):
    global image_buffer

    print(f"📩 Mensaje recibido ({len(msg.payload)} bytes)")

    if msg.payload == b"START":
        image_buffer = bytearray()
        print("🟢 Inicio imagen")

    elif msg.payload == b"END":
        os.makedirs("static", exist_ok=True)
        with open(IMAGE_PATH, "wb") as f:
            f.write(image_buffer)
        print(f"💾 Imagen guardada ({len(image_buffer)} bytes)")

    else:
        image_buffer.extend(msg.payload)

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
    mqtt_client.publish(TOPIC_COMMAND, "CAPTURE")
    return """
    <h1>comando enviado</h1>
    <a href="/">ver la foto</a><br><br>

    """

@app.route("/photo")
def photo():
    if os.path.exists(IMAGE_PATH):
        return send_file(IMAGE_PATH, mimetype="image/jpeg")
    return "❌ No hay imagen aún"
@app.route("/solution")
def solution():
    return "<h1>aqui esta tu solucion</h1>"

if __name__ == "__main__":
    app.run(debug=True)
