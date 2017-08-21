import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class Output:
    unlock_channel = 16
    lock_channel = 18
    sensor_channel = 25

    def __init__(self):
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
        GPIO.output(self.unlock_channel, True)
        time.sleep(1)
        GPIO.output(self.unlock_channel, False)

    def lock(self):
        GPIO.output(self.lock_channel, True)
        time.sleep(1)
        GPIO.output(self.lock_channel, False)

    def is_open(self):
        return GPIO.input(self.sensor_channel)
