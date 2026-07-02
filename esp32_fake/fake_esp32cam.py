import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
TOPIC_COMMAND = "cam/esp32/command"
TOPIC_IMAGE = "cam/esp32/image"

def on_message(client, userdata, msg):
    if msg.payload == b"CAPTURE":
        print("📸 Simulando captura")

        with open("floor.jpeg", "rb") as f:
            data = f.read()

        client.publish(TOPIC_IMAGE, b"START")
        time.sleep(0.1)

        CHUNK = 1024
        for i in range(0, len(data), CHUNK):
            client.publish(TOPIC_IMAGE, data[i:i+CHUNK])
            time.sleep(0.01)

        client.publish(TOPIC_IMAGE, b"END")

client = mqtt.Client()
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC_COMMAND)
client.on_message = on_message
client.loop_forever()
