import network

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

if sta_if.active():
    sta_if.connect('SuaRede','SuaSenha')
    sta_if.ifconfig()

if not sta_if.isconnected():
    print("Ops...")
