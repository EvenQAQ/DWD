from json import load
import os
import sys
import time
from time import sleep
import datetime
import platform
# import numpy as np

from guizero import App, Picture, PushButton
from gpiozero import Button, OutputDevice, RotaryEncoder, DigitalInputDevice, InputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import scaled_half
from PIL import Image, ImageTk

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", type=str, help="input name")
parser.add_argument("-p", "--position", type=int, default=0, help="input default position")
args = parser.parse_args()
rotor_now = args.position
rotor_last = rotor_now + 1

# register GPIO
if platform. system() == "Darwin":
    # factory = PiGPIOFactory(host='192.168.0.58') # 填写树莓派的IP地址
    factory = PiGPIOFactory(host='10.126.159.234')
else:
    factory = PiGPIOFactory()

btn_rotor = Button(22, pin_factory=factory)
# rotor = RotaryEncoder(27, 17, max_steps=20, wrap=True, pin_factory=factory)

# btn_red = Button(24, pin_factory=factory)
# btn_blue = Button(23, pin_factory=factory)
touch_red = DigitalInputDevice(23, pin_factory=factory)
touch_blue = DigitalInputDevice(24, pin_factory=factory)
relay_red = OutputDevice(14, pin_factory=factory, active_high=True, initial_value=False)
relay_blue = OutputDevice(15, pin_factory=factory, active_high=True, initial_value=False)

root_dir = "./assets/"
news_dir = "./assets/news/"
feedback_dir = "./assets/feedback/"
loading_dir = "./assets/loading/"

test_welcome = root_dir + 'welcome.png'
test_news = root_dir + 'test_news.png'
test_feedback = root_dir + 'test_feedback.png'

news_pages = []
feedback_pages = [[], []]
chart_pages = []
loading_pages = []
page_num = 6
page_map= {}
valid_map = {}
change_map = {0:1, 1:0, 3:4, 4:3, 6:7, 7:6, 9:10, 10:9, 12:13, 13:12, 15:16, 16:15, 18:19, 19:18}
# change_map = {0:1, 1:0, 3:4, 4:3, 6:7, 7:6, 9:10, 10:9, 12:13, 13:12, 15:16, 16:15, 18:19, 19:18, -20:-19, -19:-20, -17:-16, -16:-17, -14:-13, -13:-14, -11:-10, -10:-11, -8:-7, -7:-8, -5:-4, -4:-5, -2:-1, -1:-2}
red_chosen = []
blue_chosen = []
last_rotate = 0
sleep_time_r = 0.6
sleep_time_b = 0.6

# load pages
for i in range(0, page_num):
    page_map[3 * i + 1] = i
    page_map[3 * i + 2] = i
    page_map[3 * i + 3] = i
    # page_map[3 * i - 19] = i
    # page_map[3 * i - 18] = i
    # page_map[3 * i - 17] = i
    valid_map[3 * i + 1] = True
    valid_map[3 * i + 2] = True
    valid_map[3 * i + 3] = True
    # valid_map[3 * i + 3] = False
    # valid_map[3 * i - 19] = True
    # valid_map[3 * i - 18] = True
    # valid_map[3 * i - 17] = False

page_map[-1] = 6
page_map[19] = 6
page_map[0] = 6
# for root, dirs, files in os.walk(pages_dir):
#     for name in files:
#         if '.png' in name:
#             news_pages.append(os.path.join(root, name))
feedback_pages[0].append(0)
feedback_pages[1].append(0)
for i in range(0, page_num):
    news_pages.append(Image.open(os.path.join(news_dir + str(i) + ".png")))
    for j in range(1, 101):
        feedback_pages[0].append(feedback_dir + str(i) + "/F" + str(j) + ".png")
        feedback_pages[1].append(feedback_dir + str(i) + "/T" + str(j) + ".png")
news_pages.append(Image.open("./assets/warning.png"))


for i in range(0, 11):
    loading_pages.append(Image.open(loading_dir + str(i) + ".jpg"))
# loading = Image.open("./assets/loading5.gif")

with open('./test.csv', "r") as f:
    red_line = f.readline()
    red_ar = red_line.split(',')
    blue_line = f.readline()
    blue_ar = blue_line.split(',')
    for i in range(0, 6):
        red_chosen.append(int(red_ar[i]))
        blue_chosen.append(int(blue_ar[i]))

print(red_chosen)
print(blue_chosen)
welcome = Image.open(test_welcome)
news_pages.append(welcome)

print(news_pages)
print(page_map)
print(red_chosen)

def return_default(start_time, end_time):
    if (end_time - start_time).seconds > 5:
        news_pic.image = welcome




def next_news():
    global rotor_now
    rotor_now += 1
    news_pic.image = news_pages[rotor_now]
    return news_pages[rotor_now]

def last_news():
    global rotor_now
    rotor_now -= 1
    news_pic.image = news_pages[rotor_now]
    return news_pages[rotor_now]

def calc_feedback(num1, num2):
    return 100 * num1/(num1 + num2)

# def red_touched():
#     global last_rotate
#     if last_rotate == 1:
#         last_rotate = 0
#         if valid_map[rotor.value * 20]:
#             print("red touched")
#             red_chosen[page_map[rotor.value * 20]] += 1

#             relay_red.on()
#             sleep(sleep_time_r)
#             relay_red.off()
#             prop = calc_feedback(red_chosen[page_map[rotor.value * 20]], blue_chosen[page_map[rotor.value * 20]])
#             for i in range(0, 11):
#                 news_pic.image = loading_pages[i]
#                 sleep(0.8)
#             news_pic.image = feedback_pages[0][int(prop)]
#             print("red: blue = " , prop)
#         else:
#             print("position error")

def red_pressed():
    red_chosen[rotor_now] += 1
    prop = calc_feedback(red_chosen[page_map[rotor_now]], blue_chosen[page_map[rotor_now]])
    for i in range(0, 11):
        news_pic.image = loading_pages[i]
        sleep(0.5)
    news_pic.image = feedback_pages[0][int(prop)]
    print("red: blue = " , prop)

def blue_pressed():
    blue_chosen[rotor_now] += 1
    prop = calc_feedback(red_chosen[page_map[rotor_now]], blue_chosen[page_map[rotor_now]])
    for i in range(0, 11):
        news_pic.image = loading_pages[i]
        sleep(0.5)
    news_pic.image = feedback_pages[0][int(prop)]
    print("red: blue = " , prop)

# def blue_touched():
#     global last_rotate
#     if last_rotate == 1:
#         last_rotate = 0
#         print("blue touched")
#         if valid_map[rotor.value * 20]:
#             blue_chosen[page_map[rotor.value * 20]] += 1

#             relay_blue.on()
#             sleep(sleep_time_b)
#             relay_blue.off()
#             prop = calc_feedback(blue_chosen[page_map[rotor.value * 20]], red_chosen[page_map[rotor.value * 20]])
#             for i in range(0, 11):
#                 news_pic.image = loading_pages[i]
#                 sleep(0.8)
#             news_pic.image = feedback_pages[1][int(prop)]
#             print("blue: red = " , prop)
#         else:
#             print("position error")


def pic_clicked(event):
    mouse_x = event.x
    mouse_y = event.y
    if mouse_x < 400:
        blue_pressed()
    else:
        red_pressed()

def rotor_pressed():
    print("rotor pressed")
    # next_news()

def check_change(r1, r2):
    if r1 in change_map and change_map[r1] == r2:
        return True
    return False

# def rotor_rotated():
#     global last_rotate
#     last_rotate = 1
#     global rotor_last
#     global rotor_now
#     # reset value
#     if rotor.value == 1:
#         rotor.value = 0
#     if rotor.value == -1:
#         rotor.value = 0
#     rotor_now = rotor.value * 20
#     print("rotor rotated", rotor_now)
#     if check_change(rotor_now, rotor_last):
#         news_pic.image = news_pages[page_map[rotor.value * 20]]
#     rotor_last = rotor.value * 20


# def calibrate(n):
#     rotor.value = n/20

def goodbye():
    with open(args.name +'.csv', "w") as f:
        for i in red_chosen:
            f.write(str(i))
            f.write(', ')
        f.write('\n')
        for i in blue_chosen:
            f.write(str(i))
            f.write(', ')
        f.write('\n')

    # np.save("true-" + datetime.now().date().isoformat() +'.npy', blue_chosen)
    # np.save("false-" + datetime.now().date().isoformat() +'.npy', red_chosen)
    app.destroy()


# calibrate(rotor_now)

# GUI app start
app = App(title="guizero", width=800, height=480)
app.set_full_screen()

# intro = Text(app, text="Welcome to InfoClinic", size=40, font="Monaco", color="lavender")
# text_box = TextBox(app)
# ok = PushButton(app, command=text_update, text="mes")

news_pic = Picture(app, image=welcome, width=800, height=480)
news_pic.when_left_button_pressed = next_news
news_pic.when_right_button_pressed = last_news
news_pic.when_click = pic_clicked
# btn_red = PushButton(app, command=red_touched, visible=False)
# btn_blue = PushButton(app, command=blue_touched, visible=False)

# btn_rotor.when_pressed = rotor_pressed
# rotor.when_rotated = rotor_rotated
# rotor.when_rotated_clockwise = next_news
# rotor.when_rotated_counter_clockwise = last_news
touch_red.when_activated = red_pressed
touch_blue.when_activated = blue_pressed

app.when_closed = goodbye
app.display()

