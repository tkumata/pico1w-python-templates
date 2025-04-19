import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
