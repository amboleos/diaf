import pyaudio, sys, socket
 
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 15000
timer = 0
 
p = pyaudio.PyAudio()
 
stream = p.open(format = FORMAT,channels = CHANNELS,rate = RATE,input = True,output = True,frames_per_buffer = chunk)
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(),5000))
server_socket.listen(5)
 
print "Your IP address is: ", socket.gethostbyname(socket.gethostname())
print "Server Waiting for client on port 5000"
 
while 1:
 
    client_socket, address = server_socket.accept()
    client_socket.sendall(stream.read(chunk))
