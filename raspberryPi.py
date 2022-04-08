from json import load
import os
import sys
import time
from time import sleep
import platform

from guizero import App, Picture, PushButton
from gpiozero import Button, OutputDevice, RotaryEncoder, DigitalInputDevice, InputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import scaled_half
from PIL import Image, ImageTk


# register GPIO
if platform. system() == "Darwin":
    # factory = PiGPIOFactory(host='192.168.0.58') # 填写树莓派的IP地址
    factory = PiGPIOFactory(host='10.126.159.234')
else:
    factory = PiGPIOFactory()

btn_rotor = Button(22, pin_factory=factory)
rotor = RotaryEncoder(27, 17, max_steps=20, wrap=True, pin_factory=factory)

# btn_red = Button(24, pin_factory=factory)
# btn_blue = Button(23, pin_factory=factory)
touch_red = DigitalInputDevice(23, pin_factory=factory)
touch_blue = DigitalInputDevice(24, pin_factory=factory)
relay_red = OutputDevice(14, pin_factory=factory, active_high=True, initial_value=False)
relay_blue = OutputDevice(15, pin_factory=factory, active_high=True, initial_value=False)

root_dir = "./assets/"
news_dir = "./assets/news/"
feedback_dir = "./assets/feedback/"
loading_dir = "./assets/laoding/"

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
red_chosen = [0 for i in range(0, page_num)]
blue_chosen = [0 for i in range(0, page_num)]
last_rotate = 0
rotor_last = 0
rotor_now = 0
sleep_time = 0.6

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

print(news_pages)
print(page_map)
print(red_chosen)


def route_pages():
    news_pic.image = news_pages[page_num]

def next_news():
    global page_num
    page_num += 1
    news_pic.image = news_pages[page_num]
    return news_pages[page_num]

def last_news():
    global page_num
    page_num -= 1
    news_pic.image = news_pages[page_num]
    return news_pages[page_num]

def calc_feedback(num1, num2):
    return 100 * num1/(num1 + num2)

def red_touched():
    global last_rotate
    if last_rotate == 1:
        last_rotate = 0
        if valid_map[rotor.value * 20]:
            print("red touched")
            red_chosen[page_map[rotor.value * 20]] += 1

            relay_red.on()
            sleep(sleep_time)
            relay_red.off()
            prop = calc_feedback(red_chosen[page_map[rotor.value * 20]], blue_chosen[page_map[rotor.value * 20]])
            for i in range(0, 11):
                news_pic.image = loading_pages[i]
                sleep(0.8)
            sleep(6)
            news_pic.image = feedback_pages[0][int(prop)]
            print("red: blue = " , prop)
        else:
            print("position error")

def blue_touched():
    global last_rotate
    if last_rotate == 1:
        last_rotate = 0
        print("blue touched")
        if valid_map[rotor.value * 20]:
            blue_chosen[page_map[rotor.value * 20]] += 1

            relay_blue.on()
            sleep(sleep_time)
            relay_blue.off()
            prop = calc_feedback(blue_chosen[page_map[rotor.value * 20]], red_chosen[page_map[rotor.value * 20]])
            for i in range(0, 11):
                news_pic.image = loading_pages[i]
                sleep(0.8)
            sleep(6)
            news_pic.image = feedback_pages[1][int(prop)]
            print("blue: red = " , prop)
        else:
            print("position error")

def rotor_pressed():
    print("rotor pressed")
    # next_news()

def check_change(r1, r2):
    if r1 in change_map and change_map[r1] == r2:
        return True
    return False

def rotor_rotated():
    global last_rotate
    last_rotate = 1
    global rotor_last
    global rotor_now
    # reset value
    if rotor.value == 1:
        rotor.value = 0
    if rotor.value == -1:
        rotor.value = 0
    rotor_now = rotor.value * 20
    print("rotor rotated", rotor_now)
    if check_change(rotor_now, rotor_last):
        news_pic.image = news_pages[page_map[rotor.value * 20]]
    rotor_last = rotor.value * 20


def calibrate():
    rotor.value = -1/20

def goodbye():
    app.destroy()


calibrate()

# GUI app start
app = App(title="guizero", width=800, height=480)
app.set_full_screen()

# intro = Text(app, text="Welcome to InfoClinic", size=40, font="Monaco", color="lavender")
# text_box = TextBox(app)
# ok = PushButton(app, command=text_update, text="mes")
welcome = Image.open(test_welcome)
news_pic = Picture(app, image=welcome, width=800, height=450)
# news_pic.when_left_button_pressed = route_pages
# news_pic.when_right_button_pressed = last_news
# btn_red = PushButton(app, command=red_touched, visible=False)
# btn_blue = PushButton(app, command=blue_touched, visible=False)

btn_rotor.when_pressed = rotor_pressed
rotor.when_rotated = rotor_rotated
# rotor.when_rotated_clockwise = next_news
# rotor.when_rotated_counter_clockwise = last_news
touch_red.when_activated = red_touched
touch_blue.when_activated = blue_touched

app.when_closed = goodbye
app.display()

