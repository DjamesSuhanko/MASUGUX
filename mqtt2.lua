print("Running file mqtt")
tmr.delay(100000)

gpio12 = 6

gpio.mode(gpio12,gpio.OUTPUT)
gpio.write(gpio12,gpio.LOW)

gpio13 = 7
gpio.mode(gpio13,gpio.OUTPUT)
gpio.write(gpio13.gpio.LOW)

--mqtt.Client(clientid, keepalive secs [, username, password, cleansession])
m = mqtt.Client("nodemcu",120,"swqzxzhr","9JMcxVeUNz3t")

-- last will e testamento, blabla, nao se incomode:
m:lwt("/lwt","offline",0,0)

m:on("connect",function(client)print("connected")end)
m:on("offline",function(client)print("offline")end)

-- evento do on_publish recebido...
m:on("message",function(conn,topic,data)
    print(topic..":")
    if topic == "light1" then
        if data == "ON" then
            print("received message: ON@light1")
            gpio.write(gpio12,gpio.HIGH)
        else
            print("receive OFF liked data in light1")
            gpio.write(gpio12,gpio.LOW)
        end
    else
        if topic == "Light2" then
            print("received message: ON@light2")
            gpio.write(gpio13.gpio.HIGH)
        else
            print("received OFF liked data in light2")
            gpio.write(gpio13,gpio.LOW)
        end
    end
  end
end)

m:connect("m11.cloudmqtt.com",19311,0,funtion(conn)
    print("connected")
    m:subscribe({["Light1"]=0,["Light2"]=0},function(conn)
        print("subscribe Light 1 and 2 sucess")
    end)
end)
