#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import pyaudio,wave

"""
    File name: tcp-streaming-unicast-client-audio.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 05/08/2016
    License: MIT
    Python Version: 2.7
    Code guide line: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "05/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

# Pyaudio Initialization
CHUNK = 1024
CHANNELS = 2
RATE = 16000
INPUT = True
RESPEAKER_WIDTH = 2

# Socket Initialization
HOST = '192.168.1.43'
PORT = 65000
SIZE = 1024

if __name__ == '__main__':
    '''PyAudio initialization'''
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=INPUT,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)

    '''Socket server initialization'''
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))

    for i in range(0, int(RATE / CHUNK * 10)):
        data = stream.read(CHUNK)
        connection.send(data)

    connection.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
