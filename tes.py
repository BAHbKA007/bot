import time, pyautogui, win32gui, os, re, math
from PIL import Image,ImageGrab

wins = []
proc = []
win32gui.EnumWindows(lambda x, y: y.append(x), wins)
for winId in wins:
    winName = win32gui.GetWindowText(winId)
    if winName == 'Lineage II':
        proc.append(winId)

path = str(os.path.dirname(__file__)) + '\\'
win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

print(pyautogui.locateCenterOnScreen(path + 'pic\\disc.png', region=(win_pos_x + 258, win_pos_y + 270,40,40),grayscale=True, confidence=.9))
