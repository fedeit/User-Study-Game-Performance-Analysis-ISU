import math
import serial
import time
import pyautogui

arduino_mouse = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
time.sleep(1)
arduino_mouse.flush()
time.sleep(1)

'''arduino_keyboard = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
time.sleep(1)
arduino_keyboard.flush()
time.sleep(1)'''

def write_read(x):
    arduino_mouse.flush()
    arduino_mouse.write(bytes(x, 'utf-8'))
    time.sleep(1)
    for _ in range(3):
        data = arduino_mouse.readline()
        #print(data)
    return data

def action2id(action):
    m = ['click', 'moveTo', 'doubleClick', 'keyDown', 'keyUp', 'press']
    return m.index(action) + 1

def getRelative(x, y):
     xm, ym = pyautogui.position()
     return x - xm, y - ym

def click(xo, yo):
    x, y = getRelative(xo, yo)
    write_read(f'{action2id("click")},{x},{y}')
'''
    while abs(x) >= 5 or abs(y) >= 5:
        x, y = getRelative(xo, yo)
        write_read(f'{action2id("click")},{x},{y}')'''

def moveTo(xo, yo):
    x, y = getRelative(xo, yo)
    write_read(f'{action2id("moveTo")},{x},{y}')

    '''while abs(x) >= 10 or abs(y) >= 10:
        x, y = getRelative(xo, yo)
        write_read(f'{action2id("moveTo")},{x},{y}')'''

def doubleClick(xo, yo):
    x, y = getRelative(xo, yo)
    write_read(f'{action2id("doubleClick")},{x},{y}')

    '''while abs(x) >= 5 or abs(y) >= 5:
        x, y = getRelative(xo, yo)
        write_read(f'{action2id("doubleClick")},{x},{y}')'''

def keyDown(key):
    write_read(f'{action2id("keyDown")},{key}')

def keyUp(key):
    write_read(f'{action2id("keyUp")},0,0,{key}')

def press(key):
    write_read(f'{action2id("press")},0,0,{key}')
