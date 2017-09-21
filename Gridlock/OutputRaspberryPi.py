import time
import RPi.GPIO as GPIO


class OutputRaspberryPi:
    unlock_channel = 37
    lock_channel = 38
    sensor_channel = 22
    handler = None

    def __init__(self):
        if GPIO is not None:
            GPIO.setwarnings(False)
            GPIO.cleanup()

            # Use Raspi GPIO Pin Numbers
            GPIO.setmode(GPIO.BOARD)

            # Unlock Relay
            GPIO.setup(self.unlock_channel, GPIO.OUT, initial=GPIO.HIGH)

            # Lock Relay
            GPIO.setup(self.lock_channel, GPIO.OUT, initial=GPIO.HIGH)

            # Door Sensor
            GPIO.setup(self.sensor_channel, GPIO.IN)

            # Add an interrupt trigger
            GPIO.add_event_detect(self.sensor_channel, GPIO.BOTH, self.handle_sensor)

    def unlock(self):
        if GPIO is not None:
            self.pulse_channel(self.unlock_channel)
        print 'Unlocking...'

    def lock(self):
        if GPIO is not None:
            self.pulse_channel(self.lock_channel)
        print 'Locking...'

    def handle_sensor(self, pin):
        state = GPIO.input(self.sensor_channel)

        if self.handler is not None:
            self.handler(state)

    def set_handler(self, handler):
        self.handler = handler

    def clear_handle(self):
        self.handler = None

    def is_open(self):
        if GPIO is not None:
            return GPIO.input(self.sensor_channel)

    def pulse_channel(self, channel, seconds=0.25):
        GPIO.output(channel, False)
        time.sleep(seconds)
        GPIO.output(channel, True)

