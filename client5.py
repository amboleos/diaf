    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import pyaudio
import asyncio
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
listening = False

async def rainbow(status):
    while True :
        
        MY_CYCLE = colorschemes.TheaterChase(num_led=NUM_LED, pause_value=0.04,
                                        num_steps_per_cycle=35, num_cycles=5)
        MY_CYCLE.start()

async def white(status):
    while True:

        MY_CYCLE = colorschemes.Solid(num_led=NUM_LED, pause_value=3,
                                    num_steps_per_cycle=1, num_cycles=1)
        MY_CYCLE.start()

p = pyaudio.PyAudio()

async def echo_server(reader, writer):
    global listening,p
    try:
        listening = True
        print ("listening:",listening)

        print ("\nwelcome\n",writer._transport.get_extra_info('peername'))

        stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        output=OUTPUT)

        while True:
            data = await reader.read(CHUNK)  # Max number of bytes to read
            # data = conn.recv(SIZE)

            if not data:
                break
            stream.write(data)
            # await writer.drain()  # Flow control, see later

        stream.stop_stream()
        stream.close()
        listening =False
        print ("listening:",listening)
        await asyncio.sleep(0)
    except Exception as e:
        print ("server:",e)
    finally:
        pass

    # p.terminate()

async def send_sound():
    print("we are in")
    global listening
     
    while True:
        
        await asyncio.sleep(0)

        if not GPIO.input(BUTTON) and not listening:
            print ("listening:",listening)

            
            stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=INPUT,
                input_device_index=2,
                frames_per_buffer=CHUNK)
            '''Socket server initialization'''
            # connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection.connect((HOST, PORT))

            reader, writer = await asyncio.open_connection(HOST2, PORT)

            if(listening):
                print("Listening değil Algılandı!! Kapanıyor")

                writer.close()
                await writer.wait_closed()

                stream.stop_stream()
                stream.close()
                # p.terminate()
                print("Kapandı")
            else:

                print('Three Seconds of white light')

                try:    
                    while( not GPIO.input(BUTTON) and not listening ):
                        data = stream.read(CHUNK)
                        writer.write(data)
                        await writer.drain()
                        if(listening):
                            break
                    
                    if( not listening):
                        for i in range(5):
                            data = stream.read(CHUNK)
                            writer.write(data)
                            await writer.drain()
                            if(listening):
                                break

                    writer.close()
                    await writer.wait_closed()

                    stream.stop_stream()
                    stream.close()
                    # p.terminate()
                    print("terminated")
                except Exception as e: 
                    print ("send_sound:",e)
                    writer.close()
                    await writer.wait_closed()
                    # p.terminate()
                    # p = pyaudio.PyAudio()
            

        
            
    return None

async def main(host, port):
    print ("start")
    server = await asyncio.start_server(echo_server, host, port)


    loop = asyncio.get_event_loop()
    print (loop)
    task = asyncio.create_task(send_sound())

    print ("loop,future:",loop,task)

    async with server:
        await asyncio.gather(
            server.serve_forever(), task )
    # await server.serve_forever()


asyncio.run(main(HOST1, PORT))