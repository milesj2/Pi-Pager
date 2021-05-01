import serial
import serial.tools.list_ports
# import RPi.GPIO as GPIO
import os, time

port = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=1)


def str_encode(string):
    return bytes(string, 'UTF-8')


def send_receive(string):
    port.write(str_encode(string))
    rcv = port.readline()
    # print(rcv, rcv.decode("UTF8"))
    print(rcv)
    time.sleep(1)


def send_test():
    send_receive('AT+CMGS="+447421301373"\r\n')
    send_receive('Hello User' + '\r\n')
    send_receive("\x1A")



def call():
    port.write(str_encode('ATD07421301373;\n'))
    rcv = port.readline()
    print(rcv)


def send_sms(self,destno,msgtext):
    result = port.write('AT+CMGS="+447421301373"\r\n', 99, 5000, msgtext+'\x1A')
    if result and result=='>' and self.savbuf:
        params = self.savbuf.split(':')
        if params[0]=='+CUSD' or params[0] == '+CMGS':
            return 'OK'
    return 'ERROR'


# send_test()
send_receive("AT")
call()
time.sleep(1)
