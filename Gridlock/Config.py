import ConfigParser


class Config:
    config = None

    def __init__(self):
        # New instance with 'bar' and 'baz' defaulting to 'Life' and 'hard' each
        self.config = ConfigParser.SafeConfigParser({
            'device': 'COM4',
            'db_host': 'localhost',
            'db_user': 'opgridlock',
            'db_pass': None,
            'db_port': 3306,
            'db_name': 'opgridlock',
            'lockout_max': 5,
            'lockout_time': 60,
            'mqtt_host': 'localhost',
            'mqtt_port': 1883,
            'mqtt_user': '',
            'mqtt_pass': '',
        })

        self.config.read('config/config.ini')

    def get(self, section, field):
        return self.config.get(section, field)

    def getint(self, section, field):
        return self.config.getint(section, field)

    def getfloat(self, section, field):
        return self.config.getfloat(section, field)

    def getboolean(self, section, field):
        return self.config.getboolean(section, field)
