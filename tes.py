import time, pyautogui, win32gui, os, re

path = str(os.path.dirname(__file__)) + '\\'

a = pyautogui.locateAllOnScreen(path + 'pic\\14.png', grayscale=False, confidence=.9)

i = 0
for pos in a:
    i = i + 1
print(i)
