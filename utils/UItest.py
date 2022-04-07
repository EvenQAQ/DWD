from json import load
import os
import sys
import time
from time import sleep
import platform

from guizero import App, Picture, PushButton
from PIL import Image, ImageTk


root_dir = "./assets/"
news_dir = "./assets/news/"
feedback_dir = "./assets/feedback/"
pie_dir = "./assets/chart"

test_welcome = root_dir + 'welcome.png'
test_news = root_dir + 'test_news.png'
test_feedback = root_dir + 'test_feedback.png'

news_pages = []
feedback_pages = [[], []]
chart_pages = []
page_num = 6
page_map= {}
valid_map = {}
change_map = {}
red_chosen = [0 for i in range(0, page_num)]
blue_chosen = [0 for i in range(0, page_num)]
last_rotate = 0
rotor_value = 0

sleep_time = 0.6
def load_pages():
    for i in range(0, page_num):
        page_map[3 * i + 1] = i
        page_map[3 * i + 2] = i
        page_map[3 * i + 3] = i
        page_map[3 * i - 19] = i
        page_map[3 * i - 18] = i
        page_map[3 * i - 17] = i
        valid_map[3 * i + 1] = True
        valid_map[3 * i + 2] = True
        valid_map[3 * i + 3] = False
        valid_map[3 * i - 19] = True
        valid_map[3 * i - 18] = True
        valid_map[3 * i - 17] = False

    page_map[-1] = 6
    page_map[19] = 6
    page_map[0] = 6
    # for root, dirs, files in os.walk(pages_dir):
    #     for name in files:
    #         if '.png' in name:
    #             news_pages.append(os.path.join(root, name))
    for i in range(0, page_num):
        news_pages.append(os.path.join(news_dir + str(i) + ".png"))
        for j in range(1, 101):
            feedback_pages[0].append(feedback_dir + str(i) + "/F" + str(j) + ".png")
            feedback_pages[1].append(feedback_dir + str(i) + "/T" + str(j) + ".png")
    news_pages.append("./assets/warning.png")



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
    if num2 == 0:
        return 100
    else:
        return num1/num2*100

def red_touched():
    if last_rotate == 1:
        last_rotate = 0
        if valid_map[rotor_value * 20]:
            print("red touched")
            red_chosen[page_map[rotor_value * 20]] += 1
            sleep(sleep_time)
            prop = calc_feedback(red_chosen[page_map[rotor_value * 20]], blue_chosen[page_map[rotor_value * 20]])
            news_pic.image = feedback_pages[0][int(prop)]
            print("red: blue = " , prop)
        else:
            print("position error")

def blue_touched():
    if last_rotate == 1:
        last_rotate = 0
        print("blue touched")
        if valid_map[rotor_value * 20]:
            blue_chosen[page_map[rotor_value * 20]] += 1
            relay_blue.on()
            sleep(sleep_time)
            relay_blue.off()
            prop = calc_feedback(blue_chosen[page_map[rotor_value * 20]], red_chosen[page_map[rotor_value * 20]])
            news_pic.image = feedback_pages[1][int(prop)]
            print("blue: red = " , prop)
        else:
            print("position error")

def rotor_pressed():
    print("rotor pressed")
    # next_news()

def rotor_rotated():
    last_rotate = 1
    print("rotor rotated", rotor_value * 20)
    # reset value
    if rotor_value == 1:
        rotor_value = 0
    if rotor_value == -1:
        rotor_value = 0
    news_pic.image = news_pages[page_map[rotor_value * 20]]

def calibrate():
    rotor_value = 0

def goodbye():
    app.destroy()
# main GUI
load_pages()

print(news_pages)
print(page_map)
print(red_chosen)
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
# rotor.when_rotated_clockwise = next_news
# rotor.when_rotated_counter_clockwise = last_news
touch_red.when_activated = red_touched
touch_blue.when_activated = blue_touched

app.when_closed = goodbye
app.display()

