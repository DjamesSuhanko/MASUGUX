try:
    import usocket as socket
except:
    import socket

from machine import Pin

relay = Pin(4,Pin.OUT)

html = """<!DOCTYPE html>
<html>
    <head>
        <title>Yunshan Interface by MASUGUX</title>
        <script>
            var ON  = 1;
            var OFF = 0;
            function turnRelay(state){
                if (state == ON){
                    var location_now = window.location.hostname;
                    window.location.replace("/?relay=on");
                }
                else if (state == OFF){
                    var location_now = window.location.hostname;
                    window.location.replace("?relay=off");
                }
            }
        </script>
    </head>
    <body>
        <h1>Interface de controle</h1>
    <br>
    <h3>MASUGUX e Do bit Ao Byte</h3>
        <table border="0">
          <tr>
              <th>
              <button type="button" onclick="turnRelay(ON)">Ligar</button>
              </th>
              <th>
              <button type="button" onclick="turnRelay(OFF)">Desligar</button>
              </th>
          </tr>
        </table>
    </body>
</html>
"""

request_method  = ""
path            = ""
request_version = ""


def parse_request(text):
        if text != '':
            request_line = text.split("\r\n")[0]
            request_line = request_line.split()
            print(request_line)
            # Break down the request line into components
            (request_method,  # GET
             path,            # /hello
             request_version  # HTTP/1.1
             ) = request_line
            print("Method:", request_method)
            print("Path:", path)
            print("Version:", request_version)
            if request_method == "POST":
                pass
            if request_method == "GET":
                if "?" in path:
                    #este values tem apenas o resultado final
                    filename, values = path.strip('/').split('?')
        
                    if values == 'relay=on':
                        print("Ligando rele")
                        relay.high()
                        
                    elif values == 'relay=off':
                        print("Desligando rele")
                        relay.low()

def startServer():
    s  = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>/")
    print("v4.2")
    
    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]

        try:
            header, content = parse_request(client_s.recv(4096).decode('utf-8'))
            print('length of content:' + str(len(content)))
            print (client_addr)
            if header != '':
                client_s.send(header)
                client_s.send(content)
        except:
            "oh-oh..."
            pass
            
        client_s.send(html)
        client_s.close()
