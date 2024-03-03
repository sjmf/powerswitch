#
# This is a picoweb example showing handling of HTTP Basic authentication.
#
import ulogging
import ubinascii
import uasyncio
import picoweb
import machine
import time

DEBUG=True

HOST="0.0.0.0"
PORT=80

USERNAME = "admin"
PASSWORD = "password"

app = picoweb.WebApp(None)
log = ulogging.getLogger("picoweb")

# GPIO Control
write_pin = machine.Pin(5, machine.Pin.OUT, value=0)
read_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

#
# Decorator for HTTP Basic Auth
def require_auth(func):
    UNAUTHORIZED_STATUS = "401 Unauthorized"

    def auth(req, resp):
        auth = req.headers.get(b"Authorization")
        if not auth:
            yield from resp.awrite(
                'HTTP/1.0 401 Unauthorized\r\n'
                'WWW-Authenticate: Basic realm="ESP8266"\r\n'
                '\r\n')
            return

        auth = auth.split(None, 1)[1]
        auth = ubinascii.a2b_base64(auth).decode()
        req.username, req.passwd = auth.split(":", 1)

        if req.username == USERNAME and req.passwd == PASSWORD:
            yield from func(req, resp)
        else:
            yield from picoweb.start_response(resp, status=UNAUTHORIZED_STATUS)
            yield from resp.awrite(UNAUTHORIZED_STATUS)
            yield from resp.awrite("\r\n")

    return auth


#
# Main route
@app.route("/")
@require_auth
def index(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")

    log.info(str(req))
    with open('static/control.html', 'r') as f:
        for line in f:
            yield from resp.awrite(line)


# 
# GPIO Control route
@app.route("/led")
@require_auth
def led_control(req, resp):

    # Parse Request body (or parameters)
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, etc.
        req.parse_qs()

    write_pin.value(int(req.form["value"]))
    yield from picoweb.start_response(resp)


#
# Bring pin high for specified duration only
@app.route("/pulse")
@require_auth
def led_pulse(req, resp):
    
    yield from req.read_form_data()
    yield from picoweb.start_response(resp)
    
    # Handle optional duration argument
    time_ms = 100
    try:
        time_ms = int(req.form['duration'])
        if time_ms < 1 or time_ms > 20000:
            log.info("duration = {}".format(time_ms))
            return
    except (TypeError, ValueError, KeyError) as e:
        log.error(e)

    # Pull pin high for specified duration
    write_pin.value(1)
    await uasyncio.sleep_ms(time_ms)
    write_pin.value(0)


# 
# Read from the read pin
@app.route("/read")
@require_auth
def readPin(req, resp):
    req.parse_qs()

    yield from picoweb.start_response(resp)
    yield from resp.awrite("{}".format(read_pin.value()))


ulogging.basicConfig(level=ulogging.INFO)

app.run(host=HOST, port=PORT, debug=DEBUG)
