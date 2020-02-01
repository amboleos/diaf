import pyaudio
import sys
import socket
 
ip = "192.168.1.241"
 
[b][/b]chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 15000
timer = 0
 
p = pyaudio.PyAudio()
 
stream = p.open(format = FORMAT,channels = CHANNELS,rate = RATE,input = True,output = True,frames_per_buffer = chunk)
 
while 1:
 
    #Create a socket connection for connecting to the server:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((str(ip),5000))
 
    #Recieve data from the server:
    data = client_socket.recv(1024)
    stream.write(data,chunk)
