import time, pyautogui, win32gui, os, re, math
from PIL import Image,ImageGrab

start_time = int(math.ceil(time.time()))

while True:
    uhrzeit = int(math.ceil(time.time()))
    if (uhrzeit - start_time) % 5 == 0 and (uhrzeit - start_time) != 0:
        print('jetzt ' + str(uhrzeit - start_time))