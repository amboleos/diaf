from collections import deque
import socket
import pyaudio
import asyncio
import numpy as np
import time
import sys

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
HOST1 = sys.argv[1]  #'192.168.1.50'
HOST2 = sys.argv[2]  #'192.168.1.40'
PORT1 = sys.argv[3]  #65001
PORT2 = sys.argv[4]  #65002

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


async def input_server(reader,writer,frames):
    data = await reader.read(CHUNK)
    frames.append(data)
    addr = writer.get_extra_info('peername')
    print(f"Received message from {addr!r}")

async def output_client(frames):
    try:
        reader, writer = await asyncio.open_connection(HOST2, PORT2)

        while True:
            asyncio.sleep(0)

            while len(frames):
                writer.write(frames.popleft())
                await writer.drain()

        writer.close()
        await writer.wait_closed()

    except Exception as e:
        print(e)
    



async def main():
    p = pyaudio.PyAudio()
    input_frames = deque()
    output_frames = deque()

    def input_callback(in_data, frame_count, time_info, status):
        input_frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def output_callback(in_data, frame_count, time_info, status):
        if(len(output_frames)):
            data = output_frames.popleft()
        else: 
            data= bytes()
        return (data, pyaudio.paContinue)

    input_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=INPUT,
        input_device_index=2,
        frames_per_buffer=CHUNK,stream_callback=input_callback)
    input_stream.stop_stream()
    input_task = asyncio.create_task(listen(input_stream))

    output_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=OUTPUT,stream_callback=output_callback)
    output_stream.stop_stream()
    output_task = asyncio.create_task(talk(output_stream))


    server = await asyncio.start_server(lambda r,w: input_server(r,w,output_frames), HOST1, PORT1)
    client = asyncio.create_task(output_client(input_frames))

    async with server:
        await asyncio.gather(
            server.serve_forever(),
            client,
            input_task, 
            output_task,
            )

    print("üsteki bitti")
    await asyncio.sleep(10)

asyncio.run(main())