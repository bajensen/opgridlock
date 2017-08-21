import serial
import re
import pymysql.cursors
import ConfigParser

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

access_query = '''
SELECT
  t.tag_id,
  t.tag_number,
  t.tag_code,
  IF(
      ta.holder_id IS NOT NULL AND
      hta.holder_type_id IS NOT NULL AND
      1=1
      , 1, 0
  ) AS is_authorized,
  IF(ta.holder_id IS NOT NULL, 1, 0) AS has_holder,
  IF(hta.holder_type_id IS NOT NULL, 1, 0) AS has_access,
  ta.holder_id,
  h.holder_name,
  h.holder_phone,
  h.holder_type_id,
  ht.holder_type_name,
  hta.weekday,
  hta.start_time,
  hta.end_time
FROM door_access.tag t
LEFT JOIN tag_assignment ta
  ON t.tag_id = ta.tag_id AND (
    ta.end_date >= NOW() OR
    ta.end_date IS NULL
  ) AND
  ta.start_date <= NOW()
LEFT JOIN holder h ON h.holder_id = ta.holder_id
LEFT JOIN holder_type ht ON h.holder_type_id = ht.holder_type_id
LEFT JOIN holder_type_access hta
  ON h.holder_type_id = hta.holder_type_id AND
  hta.weekday IN ('ANY', DATE_FORMAT(NOW(), '%%a')) AND
  hta.start_time <= CURTIME() AND hta.end_time >= CURTIME()
WHERE t.tag_code = %s
ORDER BY is_authorized DESC
'''

log_query = '''
INSERT INTO event (event_type, event_date, tag_id, details) 
VALUES (%s, NOW(), %s, %s)
'''

device = config.get('Reader', 'device')

print 'Operation Gridlock v. 0.0.1!'

ser = serial.Serial()
ser.baudrate = 9600
ser.port = device

print 'Connecting to RFID Reader at ' + device + '...'
ser.open()

print 'Connected to RFID reader!'

print 'Connecting to database...'

connection = pymysql.connect(
    host=config.get('Database', 'host'),
    user=config.get('Database', 'user'),
    password=config.get('Database', 'pass'),
    port=config.getint('Database', 'port'),
    db=config.get('Database', 'dbname'),
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8mb4'
)

print 'Connected to database!'


def log_scan(tag_id, type, details):
    with connection.cursor() as cursor:
        cursor.execute(log_query, (type, tag_id, details))
    connection.commit()


def process_scan(code):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(access_query, (code,))
            result = cursor.fetchone()
            print(result)
            if result is not None and result['is_authorized']:
                print 'Authorized!'
                log_scan(result['tag_id'], 'AUTH_OK', '')
            elif result is not None:
                print 'NOT AUTHORIZED!'
                log_scan(result['tag_id'], 'AUTH_FAIL', 'Code: ' + code)
            else:
                print 'NOT AUTHORIZED!'
                log_scan(None, 'AUTH_FAIL', 'Code: ' + code)
    except ValueError:
        print 'Error occurred checking database'

while ser.is_open:
    code = ser.readline()
    code = re.sub(r'\W+', '', code)
    print 'Checking code: ' + code
    process_scan(code)

connection.close()
ser.close()
