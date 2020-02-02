    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import pyaudio

"""
    File name: tcp-streaming-unicast-server-audio.py
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

# PyAudio configuration
CHUNK = 1024
CHANNELS = 2
RATE = 16000
OUTPUT = True
RESPEAKER_WIDTH = 2

# Server configuration
HOST = '192.168.1.43'
PORT = 65000
BACKLOG = 5
SIZE = 1024

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=OUTPUT)
    print(p.get_default_output_device_info())
    print("get_device_count(): ", p.get_device_count())

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((HOST, PORT))
    connection.listen(BACKLOG)

    conn, address = connection.accept()
    print ("welcome",conn, address)
    while True:
        data = conn.recv(SIZE)
        if data:
            stream.write(data)

    conn.close()
    stream.stop_stream()
    stream.close()
    p.terminate()