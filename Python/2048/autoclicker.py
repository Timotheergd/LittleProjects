import time
import pyautogui
import random

time.sleep(3)

def rotate():
    while 1:
        pyautogui.press('down')
        pyautogui.press('left')
        pyautogui.press('up')
        pyautogui.press('right')
        # time.sleep(0.3)

def rand():
    while 1:
        r = random.randint(0,4)
        if r == 0:
            pyautogui.press('down')
        elif r == 1:
            pyautogui.press('left')
        elif r == 2:
            pyautogui.press('up')
        elif r == 3:
            pyautogui.press('right')
    
rotate()