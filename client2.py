import pyaudio
import sys
import socket
import RPi.GPIO as GPIO
import time

print("Listening to stream")
while True:
    try:
        CHANNELS = 2
        RATE = 16000
        CHUNK = 1024
        RESPEAKER_WIDTH = 2

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("192.168.1.39", 4444))
        audio = pyaudio.PyAudio()
        print('Stream started')
        stream = audio.open(format=audio.get_format_from_width(RESPEAKER_WIDTH), 
                            channels=CHANNELS,
                            rate=RATE, 
                            output=True, 
                            frames_per_buffer=CHUNK)
        
        try:
            s.settimeout(0.5)
            data = s.recv(CHUNK)
            stream.write(data)
        except KeyboardInterrupt:
            pass

        print('Stream is done')
        s.close()
        stream.close()
        audio.terminate()
    except ConnectionRefusedError:
        pass
    except ConnectionResetError:
        pass
    time.sleep(0.5)
