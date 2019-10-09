import serial
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import threading
from unittest.mock import Mock
import time

'''Funcao generator que cria o mock da saida serial,
n e o valor do coracao setado para 1 na string'''

def mock_gen(n):
    max, now = 7, 0
    while(True):
        if(now == max):
            now = 0
            yield "\n".encode('utf-8')
        elif(now == n):
            now+=1
            yield "1".encode('utf-8')
        else:
            now+=1
            yield "0".encode('utf-8')


class Serial2osc:
    def __init__(self, ser_port ="/dev/ttyACM0", b_rate="115200", mock=False):
        if(not mock):
            self.ser = serial.Serial(
                port=ser_port,\
                baudrate=b_rate,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                    timeout=0)
        else:
            self.ser = Mock()
            self.ser.read = Mock(return_value=next(mock_gen(0)), side_effect = mock_gen(0)) # as you use a decode call
        self.run = True

    '''Faz a leitura da serial e manda a mensagem osc'''
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
    '''inicia a leitura da serial e o envio das mensagens'''
    def start(self):
        self.run = True
        threading.Thread(target=self.read_serial).start()

    '''envia a mensagem osc'''
    def sender(self, s):
        for i in range(0, len(s)):
            if(s[i] == "1"):
                msg = "/cue/"+str(i)
                print(msg)
                client.send_message(msg, "start")

    '''para tudo e fecha a serial'''
    def stop(self):
            self.run = False
            print(self.run)
            ser.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=53000, help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

s = Serial2osc(mock=True)

s.start()
time.sleep(10)
s.stop()
