import time
import paho.mqtt.client as mqtt
from Gridlock import Config, Database

config = Config()


class Check:
    def __init__(self, db):
        self.db = db

    db = None
    lockout_time = config.getint('Security', 'lockout_time')
    lockout_max = config.getint('Security', 'lockout_max')
    scan_topic = config.get('MQTT', 'mqtt_reader_scan_topic')
    reset_topic = config.get('MQTT', 'mqtt_reset_topic')
    lockout_fail_count = 0
    lockout_tsp = 0

    def on_connect(self, client, user_data, flags, result_code):
        print('Connected to MQTT with result code: ' + str(result_code))

        client.subscribe(self.scan_topic)
        client.subscribe(self.reset_topic)

    def on_message(self, client, user_data, msg):
        topic = str(msg.topic)
        code = str(msg.payload)

        if topic == self.reset_topic:
            self.lockout_fail_count = 0
            self.lockout_tsp = 0
            print 'LOCKOUT Cleared by MQTT...'

        elif topic == self.scan_topic:
            # After 5 failed reads, lockout scanning for fail_lockout seconds
            if self.lockout_fail_count == self.lockout_max:
                self.db.log_lockout(code, msg.topic)
                print 'LOCKOUT!!!!'
            # Reset lockout after fail_lockout seconds
            elif self.lockout_fail_count > self.lockout_max and self.lockout_tsp < time.time() - self.lockout_time:
                self.lockout_tsp = 0
                self.lockout_fail_count = 0
                print 'Cleared...'

            if self.lockout_fail_count < self.lockout_max:
                success = self.db.check_scan(code)
            else:
                success = False

            if success:
                mqtt_client.publish(config.get('MQTT', 'mqtt_lock_topic'), 'unlock')
                mqtt_client.publish(config.get('MQTT', 'mqtt_reader_result_topic'), 'success')
            else:
                mqtt_client.publish(config.get('MQTT', 'mqtt_reader_result_topic'), 'fail')
                self.lockout_tsp = time.time()
                self.lockout_fail_count += 1
        else:
            print 'Unrecognized topic'


db = Database(config)
check = Check(db)
mqtt_client = mqtt.Client()
mqtt_client.on_connect = check.on_connect
mqtt_client.on_message = check.on_message

mqtt_client.connect(
    config.get('MQTT', 'mqtt_host'),
    config.getint('MQTT', 'mqtt_port'),
    config.getint('MQTT', 'mqtt_keepalive')
)

mqtt_client.loop_forever()
