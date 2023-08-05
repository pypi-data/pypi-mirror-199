import time
import serial
import wave
import argparse


def init_modem_settings():
    ex = b'at\r\n'
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    time.sleep(0.5)
    print(ser.write(ex))
    time.sleep(0.5)
    print(ser.readline())
    res = (ser.readline())
    print(ser.write(b'atz3\r\n'))
    print(ser.readline())
    print(ser.readline())
    print(ser.write(b'at+fclass=0\r\n'))
    print(ser.readline())
    print(ser.readline())
    print(ser.write(b'ats0=2\r\n'))
    print(ser.readline())
    print(ser.readline())
    return


# =================================================================
def call(n):
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    num = str(n)
    print("Calling", num)
    cmd = "atd " + num + "\r\n"
    print("waiting for call to be answered")
    print(ser.write(cmd.encode()))
    print(ser.readline())
    print(ser.readline())
    time.sleep(60)
    print(ser.readline())
    print(ser.readline())
    return


# =================================================================
def answer():
    print("Answering*******************")
    global disable_modem_event_listener
    disable_modem_event_listener = True
    print("Before sleep")
    time.sleep(50)
    return


# =================================================================
def callAndRecord(n):
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    num = str(n)
    print("Calling", num)
    cmd = "atd " + num + "\r\n"
    print(ser.write(cmd.encode()))
    print(ser.readline())
    print(ser.readline())
    time.sleep(50)

    global disable_modem_event_listener
    disable_modem_event_listener = False
    CHUNK = 1024
    ring_data = b''
    modem_data_striped = b''
    status = "false"
    endtime = time.time() + 90.0  # 10 sec
    print("waiting for call to be answered")
    print(ser.write(b'at+vrx\r\n'))
    print(ser.readline())
    print(ser.readline())
    endCmd = "\x10!\r\n"
    audio_frames = []
    print("recording")
    while (time.time() < endtime):

        # Read audio data from the Modem
        audio_data = ser.read(CHUNK)
        if (audio_data == b''):
            print("b''")
        audio_data_decoded = audio_data.decode('iso-8859-1')

        # Add Audio Data to Audio Buffer
        audio_frames.append(audio_data)

    # Save the Audio into a .wav file
    print("\n Appending to audio.wav")
    wf = wave.open('audio.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(1)
    wf.setframerate(8000)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    ser.write(b'\x10!\r\n')
    print("Record Audio Msg - END")
    return


# =================================================================
def callAndPlay(n):
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    num = str(n)
    print("Calling", num)
    cmd = "atd " + num + "\r\n"
    print(ser.write(cmd.encode()))
    print(ser.readline())
    print(ser.readline())
    time.sleep(50)
    print("After sleep")
    print("waiting for call to be answered")
    print(ser.write(b'at+vrx\r\n'))
    print(ser.readline())
    print(ser.readline())
    print("Playing play.wav")
    wf = wave.open('play.wav', 'rb')
    chunk = 1024
    time.sleep(10)
    data = wf.readframes(chunk)
    while data != b'':
        ser.write(data)
        data = wf.readframes(chunk)
        # You may need to change this sleep interval to smooth-out the audio
        time.sleep(.15)
    cmd = "<DLE><ETX>\r"
    ser.write(cmd.encode())
    wf.close()

    print("closed wf")
    print("Play Audio Msg - END")

    return


# =================================================================
def answerAndRecord():
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    print("Answering*******************")
    global disable_modem_event_listener
    disable_modem_event_listener = True
    print("Before sleep")
    time.sleep(50)

    disable_modem_event_listener = False
    CHUNK = 1024
    ring_data = b''
    modem_data_striped = b''
    status = "false"
    endtime = time.time() + 90.0  # 10 sec
    print(ser.readline())
    print(ser.readline())
    endCmd = "\x10!\r\n"
    audio_frames = []
    print("recording")
    while (time.time() < endtime):

        # Read audio data from the Modem
        audio_data = ser.read(CHUNK)
        if (audio_data == b''):
            print("b''")
        audio_data_decoded = audio_data.decode('iso-8859-1')

        # Add Audio Data to Audio Buffer
        audio_frames.append(audio_data)

    # Save the Audio into a .wav file
    print("\n Appending to audio.wav")
    wf = wave.open('audio.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(1)
    wf.setframerate(8000)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    ser.write(b'\x10!\r\n')
    print("Record Audio Msg - END")
    return


# =================================================================
def answerAndPlay():
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    print("Answering*******************")
    global disable_modem_event_listener
    disable_modem_event_listener = True
    print("Before sleep")
    time.sleep(50)
    print("After sleep")
    print("Playing play.wav")
    wf = wave.open('play.wav', 'rb')
    chunk = 1024
    data = wf.readframes(chunk)
    while data != b'':
        ser.write(data)
        data = wf.readframes(chunk)
        # You may need to change this sleep interval to smooth-out the audio
        time.sleep(.15)
    cmd = "<DLE><ETX>\r"
    ser.write(cmd.encode())
    wf.close()
    print("closed wf")
    print("Play Audio Msg - END")
    return


# =================================================================
def read_data_answer(function):
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)
    global disable_modem_event_listener
    disable_modem_event_listener = False
    ring_data = b''
    modem_data_striped = b''

    endtime = time.time() + 90.0  # 1.5minute
    while (time.time() < endtime):
        print("waiting for ring")
        if not disable_modem_event_listener:
            modem_data = ser.readline()

            if (b'RING' in modem_data):

                if b'RING' in modem_data:
                    modem_data_striped = modem_data.rstrip()
                    print("modem_data_striped:  ", modem_data_striped)
                    print("ring_data:  ", ring_data)
                    print("modem_data:  ", modem_data_striped)
                    ring_data = ring_data + modem_data_striped
                    ring_count = ring_data.count(b'RING')
                    print("ring_count:  ", ring_count)
                    if ring_count == 1:
                        pass
                    elif ring_count == 2:
                        ring_data = b''
                        if (function == "play"):
                            answerAndPlay()
                        elif (function == "record"):
                            answerAndRecord()
                        else:
                            answer()
                        return

    if not b'RING' in modem_data:
        print ("Error: No Ring")
        close_modem_port()
        return


# =================================================================
def close_modem_port(action):
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5)

    print(ser.write(b'ath\r\n'))
    print(ser.readline())
    print(ser.readline())
    print("Ended the active calls")
    ser.close()
    print("Serial port closed")


# =================================================================
# Arg parsing
def main():
    parser = argparse.ArgumentParser(prog='gfg',
                                     description='This a voice modem testing script.')

    parser.add_argument('-o', default=False, help="call/answer", required=True)
    parser.add_argument('-number', nargs='+',
                        help='a mobile number')
    parser.add_argument('-f', help='record/play')

    args = parser.parse_args()
    n = args.number
    action = args.o
    function = args.f

    if args.o:
        print("\n Welcome to voice Modem testing ! \n")
        init_modem_settings()
        if args.o == "call":
            print("Function to be performed: ", function)

            if args.f:
                if (function == "play"):
                    callAndPlay(n)
                elif (function == "record"):
                    callAndRecord(n)
            else:
                call(n)

        elif args.o == "answer":
            print("Function to be performedL: ", function)
            read_data_answer(function)

    close_modem_port(action)


if __name__ == "__main__":
    main()
