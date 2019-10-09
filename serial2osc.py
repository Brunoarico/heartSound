import serial
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import threading

class Serial2osc:

    def __init__(self, ser_port ="/dev/ttyACM0", b_rate="115200"):
        self.ser = serial.Serial(
            port=ser_port,\
            baudrate=b_rate,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0)
        self.run = True

    def read_serial(self):
        line = ""
        while (self.run):
                c = self.ser.read().decode()
                if (c == '\n'):
                    print(line)
                    self.sender(line)
                    line = ""
                else:
                    line += c

    def start(self):
        self.run = True
        threading.Thread(target=self.read_serial).start()

    def sender(self, s):
        for i in range(0, len(s)):
            if(s[i] == "1"):
                msg = "/cue/"+str(i)+"/start"
                print(msg)
                client.send_message(msg)

    def stop(self):
            self.run = false
            ser.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

s = Serial2osc()
s.start()
