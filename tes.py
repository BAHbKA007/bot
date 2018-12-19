import time, pyautogui, win32gui, os, re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
from PIL import Image
from skimage.io import imread

path = str(os.path.dirname(__file__)) + '\\'

wins = []
proc = []
win32gui.EnumWindows(lambda x, y: y.append(x), wins)
for winId in wins:
    winName = win32gui.GetWindowText(winId)
    if winName == 'Lineage II':
        proc.append(winId)

# Fenster in Fordergrund bringen
win32gui.SetForegroundWindow(proc[len(proc)-1])

win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

def find_pic(a, conf=.9, x=1024, y=768, x_inner=0, y_inner=0):
    pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
    pyautogui.moveTo(pos)
    return pos

a = find_pic('ews.png',0.9,30,30,380,710)
time.sleep(2)
b = pyautogui.locateOnScreen(path + 'pic\\' + 'BEWS.png')

pyautogui.screenshot('temp.png', region=(b[0],b[1], 300, 23))
image = imread('temp.png')
negative = 255 - image
ews_count = int(pytesseract.image_to_string(negative)[42:].split(')')[0].replace(",",""))