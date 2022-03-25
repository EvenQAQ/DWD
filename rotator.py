# coding=utf-8

import time
import serial


serialPath = '/dev/cu.usbmodem1101'
ser = serial.Serial(serialPath, 9600)


line = ser.readline()
while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(line).strip())
    line = ser.readline()

# 每 10 秒向窗口写当前计算机时间
# sep = int(time.strftime("%S")) % 10
# if sep == 0:
#     ser.write("hello, I am hick, the time is : " +
#               time.strftime("%Y-%m-%d %X\n"))      # write a string
ser.close()




