Installation
============

Install the required Python Packages
------------------------------------
```
pip install pymysql pyserial paho-mqtt
```

Setup directories
-----------------
```
sudo addgroup --system opgridlock
sudo adduser --system --home /opt/opgridlock/ opgridlock --ingroup opgridlock --ingroup dialout --ingroup gpio
```

Clone git repository
--------------------
```
cd /opt/opgridlock/
sudo -u opgridlock git clone https://github.com/bajensen/opgridlock.git
```

Setup Log Directory
-------------------
```
sudo mkdir -p /var/log/opgridlock
sudo chown opgridlock:opgridlock /var/log/opgridlock
```

Configure
=========

Copy and change the example configuration
-----------------------------------------
`cp config/config.example.ini config/config.ini`

Configure supervisord
---------------------
`cp samples/opgridlock.conf /etc/supervisor/conf.d/opgridlock.conf`

