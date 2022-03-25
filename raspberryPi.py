from guizero import *

from gpiozero import Button, OutputDevice, RotaryEncoder
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import scaled_half
from time import sleep

# def text_update():
#     intro.value = text_box.value

# app = App(title="guizero")

# intro = Text(app, text="Welcome to InfoClinic", size=40, font="Monaco", color="lavender")
# text_box = TextBox(app)
# ok = PushButton(app, command=text_update, text="mes")

# app.display()


factory = PiGPIOFactory()
# factory = PiGPIOFactory(host='172.20.3.18') # 填写树莓派的IP地址
btn_rotor = Button(18, pin_factory=factory)
rotor = RotaryEncoder(15, 14, wrap=True, pin_factory=factory)

btn_red = Button(24, pin_factory=factory)
btn_blue = Button(23, pin_factory=factory)
relay_red = OutputDevice(27, pin_factory=factory, active_high=True, initial_value=False)
relay_blue = OutputDevice(22, pin_factory=factory, active_high=True, initial_value=False)
while True:
    if btn_red.is_pressed:
        print("red pressed")
        relay_red.on()
        sleep(3)
        relay_red.off()
    if btn_blue.is_pressed:
        print("blue pressed")
        relay_blue.on()
        sleep(3)
        relay_blue.off()
    if btn_rotor.is_pressed:
        print('rotary encoder pressed')
    if rotor.when_rotated():
        print(rotor.value * 16)



