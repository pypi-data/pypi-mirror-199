#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
paho-mqtt client overrider with broker mock implementation
all publish and subscribes are solved as if a broker was connected to client instances
"""

import paho.mqtt.client as mqtt
from .mock import FakeMqtt

mqtt.Client = FakeMqtt  # type: ignore
