from collections import deque
import socket
import pyaudio
import asyncio
import numpy as np
import time

from async_runcolorcycle import *

import RPi.GPIO as GPIO
from apa102_pi.colorschemes import colorschemes


NUM_LED = 430

# PyAudio configuration
CHUNK = 1024
CHANNELS = 2
RATE = 16000
OUTPUT = True
RESPEAKER_WIDTH = 2
NUM_LED = 430
INPUT = True
BACKLOG = 5
SIZE = 1024


class Diafon:
    """Diafon creates two way communication between another diafon instance via socket 
    communication. """

    def __init__(self, **kwargs):
        host1= kwargs .get('host1',None)
        host2= kwargs .get('host2',None)
        port= kwargs .get('port',None)


        if (host1):
            self.host1 = host1
        else:
            hostname = socket.gethostname()    
            IPAddr = socket.gethostbyname(hostname)    
            print("Your Computer Name is:" + hostname)    
            print("Your Computer IP Address is:" + IPAddr)  
            self.host1 =  IPAddr
        
        if(host2):
            self.host2 = host2
        else:
            #Auto detection code can be added
            #ex: nmap -p65000 --open 192.168.1.0/24
            raise ValueError
        
        if(port):
            self.port=port
        else:
            raise ValueError   

        self.button = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON, GPIO.IN)

        self.status = "idle"


    async def ligth_status():

        while True:
            await asyncio.sleep(0)

            if self.status is "idle":
                Solid_Async (num_led=NUM_LED, pause_value=3,
                            num_steps_per_cycle=1, num_cycles=1)  

            if self.status is "error":
                RoundAndRound_Async (num_led=NUM_LED, pause_value=0,
                            num_steps_per_cycle=NUM_LED, num_cycles=2)
            
            if self.status is "MY_CYCLE3":
                StrandTest_Async (num_led=NUM_LED, pause_value=0,
                                   num_steps_per_cycle=NUM_LED, num_cycles=3)
            
            if self.status is "loading":
                Rainbow_Async (num_led=NUM_LED, pause_value=0,
                                num_steps_per_cycle=255, num_cycles=1)
            
            if status is "connecting":
                TheaterChase_Async (num_led=NUM_LED, pause_value=0.04,
                                     num_steps_per_cycle=35, num_cycles=5)

    async def listen(input_stream):
        while True:
            await asyncio.sleep(0)
            if not(GPIO.input(self.button)):
                print("listening")
                try:
                    reader, writer = await asyncio.open_connection(self.host1, self.port)

                    input_stream.start_stream()  

                    while not(GPIO.input(self.button)):
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
        try:
            server = await asyncio.start_server(lambda r,w: talk(r,w,output_stream), HOST1, PORT)
        except:
            while True:
                await error.start()
                try:
                    server = await asyncio.start_server(lambda r,w: talk(r,w,output_stream), HOST1, PORT) 
                    break
                except:
                    print("connection not found")

        client = asyncio.create_task(listen(input_stream))

        async with server:
            await asyncio.gather(
                server.serve_forever(),
                client,
                )

        print("üsteki bitti")
        await asyncio.sleep(10)

    

        


diafon=Diafon( host1= "192.168.1.50",host2='192.168.1.150', )
asyncio.run(diafon.main())


while True:
    pass