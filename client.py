import pyaudio, sys, socket
 
# ~ chunk = 1024
# ~ FORMAT = pyaudio.paInt16
# ~ CHANNELS = 1
# ~ RATE = 15000
# ~ timer = 0

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output_with_diff.wav"

p = pyaudio.PyAudio()

# ~ stream = p.open(format = FORMAT,
                # ~ channels = CHANNELS,
                # ~ rate = RATE,
                # ~ input = True,
                # ~ output = True,
                # ~ frames_per_buffer = chunk)

stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(),5000))
server_socket.listen(5)
 
print "Your IP address is: ", socket.gethostbyname(socket.gethostname())
print "Server Waiting for client on port 5000"
 
while 1:
 
    client_socket, address = server_socket.accept()
    client_socket.sendall(stream.read(chunk))
