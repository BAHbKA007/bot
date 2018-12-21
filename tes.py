import time, pyautogui, win32gui, os, re
from PIL import Image,ImageGrab

start_time = int(str(time.time())[0:10])

while True:
    uhrzeit = int(str(time.time())[0:10])
    if (uhrzeit - start_time) % 5 == 0 and (uhrzeit - start_time) != 0:
        print('jetzt ' + str(uhrzeit - start_time))