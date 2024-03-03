# powerswitch
Remote power switch for PC using ESP8266.

This project uses micropython on the ESP8266 to implement a remote wifi-based power switch for my desktop PC.

The ESP is wired between the motherboard's power pin headers and the power button, allowing this to pass through.

The main code is in webapp.py. This defines the API using picoweb, which is like Flask but smaller.

# Requirements

 * Micropython installed on ESP
 * Picoweb (lib included in repo)

# Author

Samantha Finnigan 2021. Licensed under MIT license.

