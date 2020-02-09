from collections import deque
import socket
import pyaudio
import asyncio
import numpy as np
import time

import RPi.GPIO as GPIO
from apa102_pi.colorschemes import colorschemes

BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
NUM_LED = 430

# PyAudio configuration
CHUNK = 1024
CHANNELS = 2
RATE = 16000
OUTPUT = True
RESPEAKER_WIDTH = 2
NUM_LED = 430
INPUT = True



# Server configuration
HOST1 = '192.168.1.50'
HOST2 = '192.168.1.40'


PORT = 65000
BACKLOG = 5
SIZE = 1024


async def listen(stream):
    while True:
        await asyncio.sleep(0)
        if not(GPIO.input(BUTTON)):
            print("listening")
            stream.start_stream()   
            while not(GPIO.input(BUTTON)):
                await asyncio.sleep(1)  
            stream.stop_stream()
            print("XXX listening")

async def talk(stream):
    while True:
        await asyncio.sleep(0.5)
        
        print("talking", time.monotonic(),stream.is_active())
        stream.start_stream()
        while stream.is_active():
            await asyncio.sleep(0.5)

        stream.stop_stream()
        print("XXX talking", time.monotonic())


async def main():
    p = pyaudio.PyAudio()
    frames = deque()
    
    def input_callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    input_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=INPUT,
        input_device_index=2,
        frames_per_buffer=CHUNK,stream_callback=input_callback)
    
    input_stream.stop_stream()

    listen_task = asyncio.create_task(listen(input_stream))

    def output_callback(in_data, frame_count, time_info, status):
        if(len(frames)):
            data = frames.popleft()
        else: 
            data= bytes()
        return (data, pyaudio.paContinue)

    output_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=OUTPUT,stream_callback=output_callback)

    output_stream.stop_stream()

    output_task = asyncio.create_task(talk(output_stream))

    await asyncio.gather(
        listen_task, output_task)

    print("üsteki bitti")
    await asyncio.sleep(10)

asyncio.run(main())