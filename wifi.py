def connect():
    import network
 
    ssid = "***REMOVED***"
    password = "***REMOVED***"
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected():
        print("Already connected to network {}".format(ssid))
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while not station.isconnected():
        pass
 
    print("Connection successful")
    print(station.ifconfig())
