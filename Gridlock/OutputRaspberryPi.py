import time
import RPi.GPIO as GPIO


class OutputRaspberryPi:
    unlock_channel = 16
    lock_channel = 18
    sensor_channel = 22

    def __init__(self):
        if GPIO is not None:
            GPIO.setwarnings(False)
            GPIO.cleanup()

            # Use Raspi GPIO Pin Numbers
            GPIO.setmode(GPIO.BOARD)

            # Unlock Relay
            GPIO.setup(self.unlock_channel, GPIO.OUT, initial=GPIO.LOW)

            # Lock Relay
            GPIO.setup(self.lock_channel, GPIO.OUT, initial=GPIO.LOW)

            # Door Sensor
            GPIO.setup(self.sensor_channel, GPIO.IN)

    def unlock(self):
        if GPIO is not None:
            self.pulse_channel(self.unlock_channel)
        print 'Unlocking...'

    def lock(self):
        if GPIO is not None:
            self.pulse_channel(self.unlock_channel)
        print 'Locking...'

    def is_open(self):
        if GPIO is not None:
            return GPIO.input(self.sensor_channel)

    def pulse_channel(self, channel, seconds=0.25):
        GPIO.output(channel, True)
        time.sleep(seconds)
        GPIO.output(channel, False)

