from json import load
import os
import sys
import time
from time import sleep

from guizero import App, Picture, PushButton
from gpiozero import Button, OutputDevice, RotaryEncoder, DigitalInputDevice, InputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import scaled_half
from PIL import Image, ImageTk


# register GPIO

factory = PiGPIOFactory()
# factory = PiGPIOFactory(host='192.168.0.58') # 填写树莓派的IP地址
# factory = PiGPIOFactory(host='10.126.159.234')
btn_rotor = Button(14, pin_factory=factory)
rotor = RotaryEncoder(15, 18, max_steps=20, threshold_steps=(3, 4), wrap=True, pin_factory=factory)

# btn_red = Button(24, pin_factory=factory)
# btn_blue = Button(23, pin_factory=factory)
touch_red = DigitalInputDevice(24, pin_factory=factory)
touch_blue = DigitalInputDevice(23, pin_factory=factory)
relay_red = OutputDevice(27, pin_factory=factory, active_high=True, initial_value=False)
relay_blue = OutputDevice(22, pin_factory=factory, active_high=True, initial_value=False)


pages_dir = './assets'
test_welcome = pages_dir + '/welcome.png'
test_news = '/Users/even/Documents/Dev/DWD/assets/test_news.png'
test_feedback = pages_dir + '/test_feedback.png'

news_pages = []
page_num = 0
page_map= {}
red_chosen = []
blue_chosen = []

def load_pages():
    for i in range(0, 6):
        page_map[3 * i] = i
        page_map[3 * i + 1] = i
        page_map[3 * i + 2] = i
    for root, dirs, files in os.walk(pages_dir):
        for name in files:
            if '.png' in name:
                news_pages.append(os.path.join(root, name))


def route_pages():
    news_pic.image = news_pages[page_num]

def next_news():
    global page_num
    page_num += 1
    if
    # news_pic.image = news_pages[page_num]
    # return news_pages[page_num]

def last_news():
    global page_num
    page_num -= 1
    news_pic.image = news_pages[page_num]
    return news_pages[page_num]

def red_touched():
    print("red touched")
    # red_chosen[page_num] += 1
    relay_red.on()
    sleep(0.8)
    relay_red.off()


def blue_touched():
    print("blue touched")
    # blue_chosen[page_num] += 1
    relay_blue.on()
    sleep(0.8)
    relay_blue.off()

def rotor_pressed():
    print("rotor pressed")
    # next_news()

def rotor_rotated():
    print("rotor rotated")
    print(rotor.value * 16)

# main GUI
load_pages()

print(news_pages)
print(page_map)
app = App(title="guizero", width=800, height=480)

# intro = Text(app, text="Welcome to InfoClinic", size=40, font="Monaco", color="lavender")
# text_box = TextBox(app)
# ok = PushButton(app, command=text_update, text="mes")
news_pic = Picture(app, image=test_welcome, width=800, height=450)
news_pic.when_left_button_pressed = route_pages
news_pic.when_right_button_pressed = last_news
btn_red = PushButton(app, command=red_touched, visible=False)
btn_blue = PushButton(app, command=blue_touched, visible=False)

btn_rotor.when_pressed = rotor_pressed
rotor.when_rotated = rotor_rotated
rotor.when_rotated_clockwise = next_news
rotor.when_rotated_counter_clockwise = last_news
touch_red.when_activated = red_touched
touch_blue.when_activated = blue_touched


app.display()

