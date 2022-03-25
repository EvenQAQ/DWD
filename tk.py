#coding=utf-8

from cgi import test
from cgitb import text
import os
import sys
import time
from PIL import Image, ImageTk
import tkinter as tk
import serial

pages_dir = './assets'
test_welcome = pages_dir + '/test_welcome.png'
test_news = '/Users/even/Documents/Dev/DWD/assets/test_news.png'
test_feedback = pages_dir + '/test_feedback.png'

news_pages = []

serialPath = '/dev/cu.usbmodem1101'



def serial_server():
    ser = serial.Serial(serialPath, 9600)

    line = ser.readline()
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S",
              time.localtime()) + str(line).strip())
        line = ser.readline()

    # 每 10 秒向窗口写当前计算机时间
    # sep = int(time.strftime("%S")) % 10
    # if sep == 0:
    #     ser.write("hello, I am hick, the time is : " +
    #               time.strftime("%Y-%m-%d %X\n"))      # write a string

def load_pages():
    for root, dirs, files in os.walk(pages_dir):
        for name in files:
            news_pages.append(os.path.join(root, name))





def route_pages(page):
    return page

def next_news():
    page_num += 1
    return news_pages[page_num]

def last_news():
    page_num -= 1
    return news_pages[page_num]


def gui():
    top = tk.Tk()
    top.title('test')  # 窗口标题

    top.resizable(False, False)  # 固定窗口大小
    windowWidth = 1280  # 获得当前窗口宽
    windowHeight = 720  # 获得当前窗口高
    screenWidth, screenHeight = top.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight,
                                    (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
    top.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    top.wm_attributes('-topmost', 1)  # 窗口置顶


    # label_img = tk.Label(top, image=img_png)
    # label_img.pack()
    img_open = Image.open(test_news)
    img_png = ImageTk.PhotoImage(img_open)
    canvas = tk.Canvas(top, width=1280, height=720)
    canvas.create_image(1200, 720, image=img_png)
    canvas.pack()


    top.mainloop()

if __name__ == '__main__':
    load_pages()
    print(news_pages)


    top = tk.Tk()
    top.title('test')  # 窗口标题

    top.resizable(False, False)  # 固定窗口大小
    windowWidth = 1280  # 获得当前窗口宽
    windowHeight = 720  # 获得当前窗口高
    screenWidth, screenHeight = top.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight,
                                    (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
    top.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    top.wm_attributes('-topmost', 1)  # 窗口置顶

    global img_png
    # img_png = tk.PhotoImage(test_news)
    img_open = Image.open(test_news)
    img_png = ImageTk.PhotoImage(img_open)
    print(type(img_png))
    label_img = tk.Label(top, image=img_png)
    label_img.pack()

    # label_text = tk.Label(top, text="please display")
    # label_text.pack()
    # img_png = tk.PhotoImage(test_news)
    # canvas = tk.Canvas(top, width=1280, height=720)
    # canvas.create_image(1200, 720, img_png)
    # canvas.pack()

    top.mainloop()
