import serial
import re


class ReaderSerial:
    ser = None

    def __init__(self, config):
        device = config.get('Reader', 'device')

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = device

        print 'Connecting to RFID Reader at ' + device + '...'

        self.ser.open()

        print 'Connected to RFID reader!'

    def read(self):
        code = self.ser.readline()
        code = re.sub(r'\W+', '', code)
        return code

    def is_open(self):
        return self.ser.is_open
