'''
  microdot es una  mini vrsion de flask
  https://microdot.readthedocs.io/en/latest/#
'''
import machine
from machine import Pin
import network
import time
import camera
from time import sleep
from mqttsimple import MQTTClient

import random



sta_if=network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print ("conectando a la red")
    sta_if.active(True)
    #inicia el proceso de conexion
    sta_if.connect("LaSalleWifi","")
    # espera conexion

    while  not sta_if.isconnected():
        time.sleep(5)
        print("Esperando Conexión...")

print ("Esta Conectado: wi-fi: ",sta_if.isconnected())
print("   La ip es: ",sta_if.ifconfig())






#Pin del led de flash
led = machine.Pin(4, machine.Pin.OUT)




    

'''
https://bhave.sh/micropython-mqtt/
https://mpython.readthedocs.io/en/v2.2.1/library/mPython/umqtt.simple.html#

ESTOS LINK SON REFERENCIA

https://github.com/eclipse/paho.mqtt.python

http://www.steves-internet-guide.com/into-mqtt-python-client/

https://pypi.org/project/paho-mqtt/

'''

# se conecta a la red




broker="test.mosquitto.org"
port="1883"
    
client_id = f'python-mqtt-{random.randint(0, 1000)}'
print("client_id: ",client_id)
#client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
client = MQTTClient(client_id=client_id,server=broker, port=port)
client.connect()


TOPIC_IMAGE="cam/esp32/image"
TOPIC_COMMAND = "cam/esp32/command"
def on_message(topico,msg):
    global n
    
    print(msg,topico)
    if True:#msg == b'CAPTURE':
        ######tomar fotos
        print(1)
        foto=1
        while (foto<2):
            print(2)
            nombre = "Cap"+str(foto)+".jpg"
            print (nombre)
            print(3)
            try:
                print(4)
                camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
                
                #Establece el brillo
                camera.brightness(-1)
                
                #Orientacion normal
                camera.flip(0)

                #Orientación normal
                camera.mirror (0)
                
                #Resolución
                camera.framesize(camera.FRAME_XGA)

                #contraste
                camera.contrast(2)
                
                #saturacion
                camera.saturation (-2)
                       
                #calidad
                camera.quality(10)
                
                # special effects
                camera.speffect(camera.EFFECT_NONE)
                 
                # white balance
                camera.whitebalance(camera.WB_NONE)
                
                #Enciende flash
                #led.value(1)
                sleep (0.5)
                
                #Captura la imagen
                img = camera.capture()
                print ("Tamaño=",len(img))
                
                
                #Apaga flash
                led.value(0)
                
                #desactivar cámara
                camera.deinit ()
               
                #Guardar la imagen en el sistema de archivos
                imgFile = open(nombre, "wb")
                imgFile.write(img)
                imgFile.close()
                
                #transmitir foto
                foto+=1
                
                sleep (10)
                
            except Exception as err:
            
                print ("Error= "+str (err))
                sleep (2)
    #############

        client.publish(TOPIC_IMAGE, b"START")
        time.sleep(0.1)

        CHUNK = 1024
        for i in range(0, len(img), CHUNK):
            client.publish(TOPIC_IMAGE, img[i:i+CHUNK])
            time.sleep(0.01)

        client.publish(TOPIC_IMAGE, b"END")
        n=1
        

client.set_callback(on_message)        
client.subscribe(TOPIC_COMMAND)
n=0
while n==0:
    
    client.check_msg()
    print("probando")
    time.sleep(2)
#client.on_message = on_message
#client.loop_forever()