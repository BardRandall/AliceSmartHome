import serial
import time

ser = serial.Serial('COM7', 57600)
time.sleep(2)


def send_byte(byte):
    ser.write(bytes(byte))
    ser.readline()


def turn_on(*args):
    for i in range(len(args)):
        send_byte(str(args[i]))
    send_byte('1')


def turn_off(*args):
    for i in range(len(args)):
        send_byte(str(args[i]))
    send_byte('0')
