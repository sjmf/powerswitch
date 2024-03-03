# powerswitch
Remote power switch for PC using ESP8266.

This project uses micropython on the ESP8266 to implement a remote wifi-based power switch for my desktop PC.

The ESP is wired between the motherboard's power pin headers and the power button, allowing this to pass through.

The main code is in webapp.py. This defines the API using picoweb, which is like Flask but smaller.

# Requirements

 * Micropython installed on ESP
 * Picoweb (lib included in repo)

# Getting Started

Refer to the [MicroPython esp8266 documentation](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html) for getting Micropython set up on your controller.
This will guide you through the process of setting up MicroPython and getting a REPL prompt.

[Adafruit ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) is the tool which I have been using to copy files to the ESP. `pip install adafruit-ampy`

To check the files already on the board:
`ampy -p /dev/tty.usbserial-A1B2C3D4 --baud 115200 ls`
(replacing the serial device with your own)

To add the files from this repo to the board:
```
ampy -p /dev/tty.usbserial-A6023LNH --baud 115200 put webapp.py
ampy -p /dev/tty.usbserial-A6023LNH --baud 115200 put wifi.py
ampy -p /dev/tty.usbserial-A6023LNH --baud 115200 put main.py
```

The static files for the website and the libraries may also be required:
```
ampy -p /dev/tty.usbserial-A6023LNH --baud 115200 put lib/
ampy -p /dev/tty.usbserial-A6023LNH --baud 115200 put lib/
```

# Development

It is likely to be desirable to ignore changes to `wifi.py` to avoid committing wifi credentials.

```
git update-index --skip-worktree wifi.py
```

# Author

Samantha Finnigan 2021. Licensed under MIT license.

