import pyaudio
import sys
import socket
 
ip = "192.168.1.39"
 
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output_with_diff.wav"
 
p = pyaudio.PyAudio()
 
# stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
#                 input=True, output=True, frames_per_buffer=chunk)

stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            # input=True,
            output = True,
            input_device_index=RESPEAKER_INDEX,
            frames_per_buffer=CHUNK)

while 1:
 
    #Create a socket connection for connecting to the server:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((str(ip),5000))
 
    #Recieve data from the server:
    data = client_socket.recv(1024)
    print('data :',data)
    stream.write(data,CHUNK)
