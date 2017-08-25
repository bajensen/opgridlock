import time


class OutputNull:
    def unlock(self):
        print 'Unlocking...'

    def lock(self):
        print 'Locking...'

    def is_open(self):
        return False

    def pause(self, seconds=0.25):
        time.sleep(seconds)
