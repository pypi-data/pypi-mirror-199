"""
paho-mqtt client mock implementation
"""

import paho.mqtt.client as mqtt

_debugmock = False
_registered_clients = {}  # type: ignore
_retain_messages = {}
_clients_count = 0
_msgids = 0


class FakeMsgInfo(mqtt.MQTTMessageInfo):
    """
    mocked message info return from publish calls, messages are delivered instantly
    """

    def wait_for_publish(self, _timeout=None):
        return True

    def is_published(self):
        return True


class FakeMqtt(mqtt.Client):
    """
    mocked mqtt client class, immediately deliver messages as if connected to a broker
    """

    def _debug(self, *fmt):
        if _debugmock:
            print(*fmt)

    def __init__(self, client_id=None, clean_session=None, userdata=None, **kwa):
        global _clients_count
        super().__init__(client_id, clean_session, userdata, *kwa)
        self._state = mqtt.mqtt_cs_new
        self.userdata = userdata
        self._started = False
        if client_id is not None:
            self.client_id = client_id
        else:
            self.client_id = f"unnamed_{_clients_count}"
            _clients_count += 1
        self.on_connect = lambda _, __, ___, ____: None
        self.on_disconnect = lambda _, __, ___: None
        self.on_message = lambda _, __, ___: None
        self._debug(
            f"[{self.client_id}] initialized fake mqtt client, ud: {self.userdata}"
        )

    def enable_logger(self, *_a, **_kwa):
        pass

    def username_pw_set(self, *_a, **_kwa):
        pass

    def connect(self, *_a, **_kwa):
        self._debug(
            f"[{self.client_id}] connect, cbs: c: {self.on_connect}, d: {self.on_disconnect}, m: {self.on_message}"
        )
        self._state = mqtt.mqtt_cs_connected
        self.on_connect(self, self.userdata, {}, 0)  # pylint: disable=not-callable

    def connect_async(self, *_a, **_kwa):
        self.connect()

    def disconnect(self, *_a, **_kwa):
        self._debug(f"[{self.client_id}] disconnect")
        self._state = mqtt.mqtt_cs_disconnecting
        self.on_disconnect(self, self.userdata, 0)  # pylint: disable=not-callable

    def loop_forever(self, *_a, **_kwa):
        if not self._started:
            self._started = True
            if self._state == mqtt.mqtt_cs_connected:
                self.connect()

    def loop_start(self, *_a, **_kwa):
        self.loop_forever(_a, _kwa)

    def loop_stop(self, *_a, **_kwa):
        self._started = False

    def publish(self, topic, payload=None, qos=0, retain=False, _properties=None):
        global _msgids
        msg = mqtt.MQTTMessage(mid=_msgids, topic=topic.encode("utf-8"))
        _msgids += 1
        if payload is not None:
            msg.payload = str(payload).encode()
        msg.retain = retain
        msg.qos = qos
        self._debug(
            f"[{self.client_id}] publishing '{topic}': "
            + "{"
            + f"mid: {msg.mid}, retain: {msg.retain}, qos: {msg.qos}, payload: {msg.payload}"
            + "}"
        )
        if retain:
            _retain_messages[topic] = msg
        for clitopic, clients in _registered_clients.items():
            if mqtt.topic_matches_sub(clitopic, topic):
                self._debug(
                    f"[{self.client_id}] found subscribed clients: {[c.client_id for c in _registered_clients[topic]]}"
                )
                for cli in clients:
                    cli.on_message(  # pylint: disable=not-callable
                        cli, cli.userdata, msg
                    )
        return FakeMsgInfo(msg.mid)

    def subscribe(self, topic, _qos=0, _options=None, _properties=None):
        self._debug(f"[{self.client_id}] subscribe {topic}")
        if isinstance(topic, tuple):
            topic = [topic]
        for topicdata in topic:
            if isinstance(topicdata, tuple):
                _topic = topicdata[0]
            else:
                _topic = topicdata
            self._debug(f"[{self.client_id}] subscribe to '{_topic}'")
            if _topic not in _registered_clients:
                _registered_clients[_topic] = set()
            _registered_clients[_topic].add(self)
            for msgtopic, msg in _retain_messages.items():
                if mqtt.topic_matches_sub(_topic, msgtopic):
                    self.on_message(  # pylint: disable=not-callable
                        self, self.userdata, msg
                    )
