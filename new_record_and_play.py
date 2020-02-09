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
listening = False

p = pyaudio.PyAudio()
frames = deque()

while GPIO.input(BUTTON):
    pass

print ("listening:")

def input_callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

input_stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=CHANNELS,
    rate=RATE,
    input=INPUT,
    input_device_index=2,
    frames_per_buffer=CHUNK,stream_callback=input_callback)

input_stream.start_stream()
while(True):
    time.sleep(0.1)
    if not(GPIO.input(BUTTON)):
        break   
print("stop!")
input_stream.stop_stream()
input_stream.close()

print ("Playing")


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

output_stream.start_stream()

while output_stream.is_active():
    time.sleep(0.1)        

output_stream.stop_stream()
output_stream.close()

p.terminate()