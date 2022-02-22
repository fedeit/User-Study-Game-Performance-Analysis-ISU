from multiprocessing.connection import wait
import pyautogui as pag
import pydirectinput as pdi
import time, os

pag.FAILSAFE = False
def waitAndLocate(path):
    c = pag.locateOnScreen(path)
    while (not c):
        c = pag.locateOnScreen(path, confidence=0.75)
    print('...found')
    return pag.center(c)

def click(pt):
    pdi.click(pt[0], pt[1])
    print(pt)
    
def dblClick(pt):
    pdi.doubleClick(pt[0], pt[1])

print(os.getcwd())
os.chdir('./scripts/GTA5')
print(os.getcwd())

print('Locating launcher')
c = waitAndLocate('./0_Launcher.PNG')
dblClick(c)

print('Locating story mode')
c = waitAndLocate('1_Story Mode.PNG')
time.sleep(2.5)
pag.moveTo(c[0], c[1], 3)
click(c)

print('Locating in game')
waitAndLocate('2_In Game.PNG')

print('Pressing esc')
pdi.press('esc')
time.sleep(2)

print('Yes exit')
c = waitAndLocate('6_Yes_Exit.PNG')
click(c)