import paho.mqtt.client as mqtt
from Gridlock import Config, ReaderSerial


def on_connect(client, user_data, flags, result_code):
    print('Connected to MQTT with result code: ' + str(result_code))

    mqtt_client.subscribe(config.get('MQTT', 'mqtt_reader_result_topic'))


def on_message(client, user_data, msg):
    result = str(msg.payload)
    print result


config = Config()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(
    config.get('MQTT', 'mqtt_host'),
    config.getint('MQTT', 'mqtt_port'),
    config.getint('MQTT', 'mqtt_keepalive')
)

reader = ReaderSerial(config)

mqtt_client.loop_start()

while reader.is_open():
    code = reader.read()
    mqtt_client.publish(config.get('MQTT', 'mqtt_reader_scan_topic'), code)
    print code
