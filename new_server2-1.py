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
HOST2 = '192.168.1.150'
PORT1 = 65000
PORT2 = 65000

PORT = 65000
BACKLOG = 5
SIZE = 1024



async def listen(input_stream):
    while True:
        await asyncio.sleep(0)
        if not(GPIO.input(BUTTON)):
            print("listening")
            try:
                reader, writer = await asyncio.open_connection(HOST2, PORT2)

                input_stream.start_stream()  

                while not(GPIO.input(BUTTON)):
                    # await asyncio.sleep(1)
                    data = input_stream.read(CHUNK)
                    # output_stream.write(data)
                    writer.write(data)
                    await writer.drain()
                
                await asyncio.sleep(0.5)
                writer.close()
                await writer.wait_closed()

                input_stream.stop_stream()
                print("XXX listening")
            except Exception as e:
                print (e)

async def talk(reader,writer,output_stream):
        await asyncio.sleep(0)
        print("talking")
        output_stream.start_stream()
        while output_stream.is_active():
            data = await reader.read(CHUNK)
            output_stream.write(data)
            await asyncio.sleep(0)
        output_stream.stop_stream()
        print("XXX talking", time.monotonic())


async def main():
    p = pyaudio.PyAudio()
    # frames = deque()
    
    # def input_callback(in_data, frame_count, time_info, status):
    #     print(f"*-* input_cb *-* {len(frames)}")
    #     frames.append(in_data)
    #     return (in_data, pyaudio.paContinue)
    # def output_callback(in_data, frame_count, time_info, status):
    #     print(f"\t\t\t *-* output_cb *-* {len(frames)}")
    #     if(len(frames)):
    #         data = frames.popleft()
    #     else: 
    #         data= bytes()
    #     return (data, pyaudio.paContinue)

    input_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=INPUT,
        input_device_index=2,
        frames_per_buffer=CHUNK,
        # stream_callback=input_callback
        )
    input_stream.stop_stream()

    output_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=OUTPUT,
                #stream_callback=output_callback
                )
    output_stream.stop_stream()

    # listen_task = asyncio.create_task(listen(input_stream))
    # output_task = asyncio.create_task(talk(input_stream,output_stream))

    server = await asyncio.start_server(lambda r,w: talk(r,w,output_stream), HOST1, PORT1)
    client = asyncio.create_task(listen(input_stream))

    async with server:
        await asyncio.gather(
            server.serve_forever(),
            client,
            )

    print("üsteki bitti")
    await asyncio.sleep(10)

asyncio.run(main())
