import ConfigParser
import sys
import time

from Gridlock import Database, Reader

# New instance with 'bar' and 'baz' defaulting to 'Life' and 'hard' each
config = ConfigParser.SafeConfigParser({
    'device': 'COM4',
    'host': 'localhost',
    'user': 'opgridlock',
    'pass': None,
    'port': 3306,
    'dbname': 'opgridlock',
    'lockout_max': 5,
    'lockout_time': 60,
})

config.read('config.ini')

print 'Operation Gridlock v. 0.0.1!'

db = Database(config)
reader = Reader(config)
op = None

lockout_time = config.getint('Security', 'lockout_time')
lockout_max = config.getint('Security', 'lockout_max')
lockout_fail_count = 0
lockout_tsp = 0

if '-n' in sys.argv:
    from Gridlock.OutputNull import OutputNull
    op = OutputNull()
else:
    from Gridlock.OutputRaspberryPi import OutputRaspberryPi
    op = OutputRaspberryPi()

while reader.is_open():
    code = reader.read()

    # After 5 failed reads, lockout scanning for fail_lockout seconds
    if lockout_fail_count == lockout_max:
        print "LOCKOUT!!!!"
    # Reset lockout after fail_lockout seconds
    elif lockout_fail_count > lockout_max and lockout_tsp < time.time() - lockout_time:
        fail_start_timestamp = 0
        lockout_fail_count = 0
        print "Cleared..."

    if lockout_fail_count < lockout_max:
        success = db.check_scan(code)
    else:
        success = False

    if success:
        op.unlock()
    else:
        lockout_tsp = time.time()
        lockout_fail_count += 1


