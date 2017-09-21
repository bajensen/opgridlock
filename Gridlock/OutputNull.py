import time


class OutputNull:
    def unlock(self):
        print 'Unlocking...'

    def lock(self):
        print 'Locking...'

    def is_open(self):
        return False

    def set_handler(self, handler):
        pass

    def clear_handle(self):
        pass

    def pause(self, seconds=0.25):
        time.sleep(seconds)
