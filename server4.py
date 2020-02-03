#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import pyaudio,wave
import asyncio
import RPi.GPIO as GPIO
from apa102_pi.colorschemes import colorschemes

BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
NUM_LED = 430

# Pyaudio Initialization
CHUNK = 1024
CHANNELS = 2
RATE = 16000
INPUT = True
RESPEAKER_WIDTH = 2

# Socket Initialization
HOST = '192.168.1.50'
PORT = 65000
SIZE = 1024




p = pyaudio.PyAudio()

                
async def send_sound():
    while True:
        if not GPIO.input(BUTTON):

            
            stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=INPUT,
                input_device_index=2,
                frames_per_buffer=CHUNK)
            '''Socket server initialization'''
            # connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection.connect((HOST, PORT))

            reader, writer = await asyncio.open_connection(HOST, PORT)

            print('Three Seconds of white light')
            
            while( not GPIO.input(BUTTON)  ):
                data = stream.read(CHUNK)
                writer.write(data)
                await writer.drain()
            
            for i in range(5):
                data = stream.read(CHUNK)
                writer.write(data)
                await writer.drain()

            writer.close()
            await writer.wait_closed()

            stream.stop_stream()
            stream.close()
            # p.terminate()
            print("terminated")

    return None

async def main():
    result = await send_sound()

asyncio.run(main())