import pymysql.cursors


class Database:
    connection = None

    def __init__(self, config):
        print 'Connecting to database...'

        self.connection = pymysql.connect(
            host=config.get('Database', 'host'),
            user=config.get('Database', 'user'),
            password=config.get('Database', 'pass'),
            port=config.getint('Database', 'port'),
            db=config.get('Database', 'dbname'),
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )

        print 'Connected to database!'

    def log_scan(self, tag_id, type, details):
        with self.connection.cursor() as cursor:
            cursor.execute(self.log_query, (type, tag_id, details))
        self.connection.commit()

    def check_scan(self, code):
        success = False
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute(self.access_query, (code,))
                result = cursor.fetchone()
                if result is not None and result['is_authorized']:
                    success = True
                    print 'Authorized!'
                    self.log_scan(result['tag_id'], 'AUTH_OK', '')
                elif result is not None:
                    print 'NOT AUTHORIZED!'
                    self.log_scan(result['tag_id'], 'AUTH_FAIL', 'Code: ' + code)
                else:
                    print 'NOT AUTHORIZED!'
                    self.log_scan(None, 'AUTH_FAIL', 'Code: ' + code)
        except ValueError:
            print 'Error occurred checking database'

        return success

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
    FROM tag t
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