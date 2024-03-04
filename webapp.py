#
# This is a picoweb example showing handling of HTTP Basic authentication.
#
from microdot import Microdot, send_file

import logging
import ubinascii
import uasyncio
import machine
import time
import ujson


def load_config():
    config = {}
    try:
        # Load config from file
        with open('config.json', 'r') as f:
            config = ujson.loads(f.read())

        cset = set(['host', 'password', 'debug', 'port', 'username'])

        if cset not in set(config.keys()):
            raise KeyError("Config missing from file. Overwriting.")
    except:
        config = {
            'debug': True,
            'host': "0.0.0.0",
            'port': 80,
            'username': "admin",
            'password': "password"
        }
        with open('config.json', 'w') as f:
            f.write(ujson.dumps(config))
    finally:
        return config

config = load_config()
log = logging.getLogger(__name__)
level = logging.DEBUG if config['debug'] else logging.INFO
logging.basicConfig(level=level)

# GPIO Control
write_pin = machine.Pin(5, machine.Pin.OUT, value=0)
read_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

log.info(config)

app = Microdot()

#
# Decorator for HTTP Basic Auth
@app.before_request
async def require_auth(req):
    log.info("{} {} {}".format(req.method, req.path, req.client_addr[0]))
    UNAUTHORIZED_STATUS = "401 Unauthorized"

    def unauthorized():
        return UNAUTHORIZED_STATUS, 401, {'WWW-Authenticate': 'Basic realm="ESP8266"'}

    def auth(req):
        auth = req.headers.get("Authorization")
        log.debug("checkauth1: {}".format(auth))
        if not auth:
            return unauthorized()

        auth = auth.split(None, 1)[1]
        auth = str(ubinascii.a2b_base64(auth).decode())
        req.username, req.passwd = auth.split(":", 1)
        log.debug("checkauth2: {} / {} / {}".format(auth, req.username, req.passwd))

        if req.username == config['username'] and req.passwd == config['password']:
            return req.username

        return unauthorized()

    user = auth(req)
    log.debug("checkauth3: {},{}".format(user, not user))
    if not user:
        return unauthorized()
    req.g.user = user


#
# Serve statics
@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path, max_age=86400)


#
# Main route
@app.route("/")
async def index(req):
    try:
        return send_file('static/control.html')
    except MemoryError as e:
        log.error(e)
    finally:
        return "Server Error", 500


# 
# GPIO Control route
#@app.route("/led")
#async def led_control(req):
#    value = 0
#    # Parse Request body (or parameters)
#    try:
#        if req.method == "POST":
#            value = int(req.form.get('value'))
#        else:  # GET, etc.
#            value = int(req.args.get('value'))
#    except:
#        # KeyError, etc
#        return 'Bad Request', 400
#
#    write_pin.value(value)
#    # return '200 OK', 200


#
# Bring pin high for specified duration only
@app.route("/pulse", methods=['GET', 'POST'])
async def led_pulse(req):
    
    # Handle optional duration argument
    time_ms = 100
    try:
        if req.method == "POST":
            time_ms = int(req.form.get('duration'))
        else: # "GET"
            time_ms = int(req.args.get('duration'))

        if time_ms < 1 or time_ms > 11000:
            log.info("duration = {}".format(time_ms))
            return 'Bad Request', 400
    except (TypeError, ValueError, KeyError) as e:
        log.error(e)

    # Pull pin high for specified duration
    write_pin.value(1)
    await uasyncio.sleep_ms(time_ms)
    write_pin.value(0)

    return 'OK', 200


# 
# Read from the read pin
@app.route("/read")
async def readPin(req):
    return "{}".format(int(read_pin.value()) ^ 1), 200

app.run(host=config['host'], port=config['port'], debug=config['debug'])
