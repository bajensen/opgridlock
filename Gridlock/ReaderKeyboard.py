from KeyboardAlike import Reader


class ReaderKeyboard:
    reader = None

    def __init__(self):
        print 'Connecting to USBHID RFID Reader...'

        self.reader = Reader(0xffff, 0x0035, 144, 16, should_reset=False)
        self.reader.initialize()

        print 'Connected to USBHID RFID reader!'

    def read(self):
        return self.reader.read().strip()

    def is_open(self):
        return True

