# python-paho-mqtt-mock

Simple [paho-mqtt](http://pypi.org/project/paho-mqtt) wrapper library implementing mqtt mocked broker for unit testing mqtt client applications.

## Install

```shell
  pip install paho-mqtt-mock
```

## Usage

Import this library first in your test main code and simply use paho-mqtt client, all publish/subscribes will be resolved immediately without the need of a real mqtt broker.

E.g. `mytest.py`
```python
   import pahomqttmock
   import paho.mqtt.client as mqtt

   def on_connect(client, userdata, flags, rc):
       print("Connected with result code "+str(rc))
   
       # Subscribing in on_connect() means that if we lose the connection and
       # reconnect then subscriptions will be renewed.
       client.subscribe("$SYS/#")
       client.subscribe("test/topic")
   
   def on_message(client, userdata, msg):
       print(msg.topic+" "+str(msg.payload))
   
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   
   client.connect("mqtt.eclipseprojects.io", 1883, 60)
   
   client.loop_start()

   client.publish("test/topic", "TEST MESSAGE")
```

## Limitations

Only mqtt `Client` class is wrapped right now, subscribers and global publish functions will not work.
