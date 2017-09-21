import sys
import paho.mqtt.client as mqtt
from Gridlock import Config

op = None

if '-n' in sys.argv:
    from Gridlock.OutputNull import OutputNull
    op = OutputNull()
else:
    from Gridlock.OutputRaspberryPi import OutputRaspberryPi
    op = OutputRaspberryPi()


def on_door_state(new_state):
    print('Door changed state: ' + new_state)

    client.publish(config.get('MQTT', 'mqtt_door_state'), new_state, True)


def on_connect(client, user_data, flags, result_code):
    print('Connected to MQTT with result code: ' + str(result_code))

    client.subscribe(config.get('MQTT', 'mqtt_lock_topic'))


def on_message(client, user_data, msg):
    action = str(msg.payload)
    if action == 'lock':
        op.lock()
    elif action == 'unlock':
        op.unlock()
#         TODO: implement open/close status check


# Set the handler
op.set_handler(on_door_state)

config = Config()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    config.get('MQTT', 'mqtt_host'),
    config.getint('MQTT', 'mqtt_port'),
    config.getint('MQTT', 'mqtt_keepalive')
)

client.loop_forever()
