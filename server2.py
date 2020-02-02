import pyaudio, sys, socket
import RPi.GPIO as GPIO
import select,time

BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

while True:
    while GPIO.input(BUTTON):
        CHANNELS = 2
        RATE = 16000
        CHUNK = 1024
        RESPEAKER_WIDTH = 2


        audio = pyaudio.PyAudio()
        print("Setting up sockets")
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(("192.168.1.39", 4444))
        serversocket.listen(5)


        def callback(in_data, frame_count, time_info, status):
            inputMode = GPIO.input(17)
            if not inputMode:
                print("Done!")
                serversocket.close()
                return (None, pyaudio.paComplete)
            else:
                for s in read_list[1:]:
                    try:
                        s.send(in_data)
                    except ConnectionResetError:
                        pass
                    except ConnectionAbortedError:
                        pass
                return (None, pyaudio.paContinue)


        # start Recording
        stream = audio.open(format=audio.get_format_from_width(RESPEAKER_WIDTH), 
                            channels=CHANNELS, 
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK, 
                            stream_callback=callback)
        stream.start_stream()

        read_list = [serversocket]
        print ("recording...")
        try:
            while GPIO.input(17):
                readable, writable, errored = select.select(read_list, [], [])
                print (readable, writable, errored)
                for s in readable:
                    if GPIO.input(17):
                        if s is serversocket:
                            (clientsocket, address) = serversocket.accept()
                            read_list.append(clientsocket)
                            print ("Connection from" + str(address))
                        else:
                            data = s.recv(1024)
                            if not data:
                                read_list.remove(s)
        except KeyboardInterrupt:
            pass
        except ConnectionResetError:
            pass

        print ("finished recording")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        time.sleep(0.5)
        
