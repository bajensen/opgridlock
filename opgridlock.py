import ConfigParser

from Gridlock import Database, Reader, Output

# New instance with 'bar' and 'baz' defaulting to 'Life' and 'hard' each
config = ConfigParser.SafeConfigParser({
    'device': 'COM4',
    'host': 'localhost',
    'user': 'opgridlock',
    'pass': None,
    'port': 3306,
    'dbname': 'opgridlock',
})

config.read('config.ini')

print 'Operation Gridlock v. 0.0.1!'

db = Database(config)
reader = Reader(config)
op = Output()

while reader.is_open():
    code = reader.read()
    success = db.check_scan(code)
    if success:
        op.unlock()
