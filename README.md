# Manage some features Mosquitto by UI

__NOTE! This project is experimental simply application as part of python learning.__

Current features is:
- manage the password file

### Run mqttUI server

```
(mqtt-ui) root@pyenv $ python3 app.py --help
usage: app.py [-h] [--host HOST] [--port PORT] [--pwd PWD]

mqttUI server start

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  Set the bind address for mqttUI (default: 0.0.0.0)
  --port PORT  Set listen on a specified port (default: 8383)
  --pwd PWD    Select path to the mosquitto password file
(mqtt-ui) root@pyenv $ python3 app.py --pwd "/etc/mosquitto/passwd"
======== Running on http://0.0.0.0:8383 ========
(Press CTRL+C to quit)
[ 2020-01-14 15:32:20 ] mqttUI: [INFO] anonymous@192.168.100.105 - GET / HTTP/1.1 302 182 0.002502
[ 2020-01-14 15:32:21 ] mqttUI: [INFO] anonymous@192.168.100.105 - GET /login HTTP/1.1 200 3453 0.020436

```

### Current view UI page

![Image](screen1.png)


## License 
The code in this repository, unless otherwise noted, is MIT licensed. See the LICENSE file for more.
