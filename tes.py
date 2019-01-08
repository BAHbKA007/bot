import time, pyautogui, win32gui, os, re, math, subprocess, psutil, traceback, win32api, win32con, requests, pytesseract
from PIL import Image,ImageGrab
from interception import ffi, lib
from skimage.io import imread
from interception.utils import raise_process_priority

start_time = int(time.time())
path = str(os.path.dirname(__file__)) + '\\'
wins = []
proc = []

#               PICTURE
#
#
#
PICTURE = 'eas.png'
#
#
if PICTURE.find('w') != -1:
    max_enchant = '18.png'
else:
    max_enchant = '14.png'
#

# Auflösung holen
desktop_size = []
for i in pyautogui.size():
    desktop_size.append(int(i/2))

win32gui.EnumWindows(lambda x, y: y.append(x), wins)
for winId in wins:
    winName = win32gui.GetWindowText(winId)
    if winName == 'Lineage II':
        proc.append(winId)

# path = str(os.path.dirname(__file__)) + '\\'
win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

# ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
# ench_window_x = ench_window[0]
# ench_window_y = ench_window[1]

# PICTURE = 'eaa.png'
# #
# #
# if PICTURE.find('w') != -1:
#     max_enchant = '18.png'
# else:
#     max_enchant = '14.png'
# #

class SCANCODE:
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002
    TAB = 0x0F
    SCANCODE_ESC = 0x01

    anmeldedaten = {
        'a' : 0x1E,
        'b' : 0x30,
        'h' : 0x23,
        'k' : 0x25,
        '0' : 0x0B,
        '1' : 0x2,
        '5' : 0x6,
        '7' : 0x8,
        '8' : 0x9,
        '9' : 0x0A
    }

def find_pic(a, conf=.9, x=800, y=600, x_inner=0, y_inner=0):
    pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
    pyautogui.moveTo(pos)
    return pos 

def anmelden(benutzer,pw):
    context = lib.interception_create_context()
    kstroke = ffi.new('InterceptionKeyStroke *')

    for key in benutzer:
        kstroke.code = SCANCODE.anmeldedaten[key]
        lib.interception_send(context, 1,  kstroke, 1)

    kstroke.code = SCANCODE.TAB
    lib.interception_send(context, 1,  kstroke, 1)

    for key in pw:
        kstroke.code = SCANCODE.anmeldedaten[key]
        lib.interception_send(context, 1,  kstroke, 1)

wins = []
proc = []

def find_proc():
    win32gui.EnumWindows(lambda x, y: y.append(x), wins)
    for winId in wins:
        winName = win32gui.GetWindowText(winId)
        if winName == 'Lineage II':
            proc.append(winId)
    return proc
def discon(address):
    return not not os.system('ping %s -n 1 > NUL' % (address,))
def mausklick():
    context = lib.interception_create_context()

    stroke = ffi.new('InterceptionMouseStroke *')
        
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    lib.interception_send(context, 11, stroke, 1)
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    lib.interception_send(context, 11,  stroke, 1)
    lib.interception_destroy_context(context)

#print(pyautogui.pixelMatchesColor(int(pyautogui.size()[0]) / 2, int(pyautogui.size()[1]) / 2, (240, 240, 240)))

# win_pos = win32gui.GetWindowRect(find_proc()[len(proc)-1])
# win_pos_x = win_pos[0] + 7
# win_pos_y = win_pos[1]



# i=10
# x=0
# a = []
# while x < i:
#     t = time.time()
#     pyautogui.locateCenterOnScreen(path + 'pic\\ok.png',grayscale=True)
#     a.append(time.time() - t)
#     x = x + 1
# print('ok.png auf ganzem Bildschirm: ' +  str(sum(a) / len(a)))

# x=0
# a = []
# while x < i:
#     t = time.time()
#     pyautogui.locateOnScreen(path + 'pic\\ok.png', region=(ench_window_x + 83, ench_window_y + 372,13,21),grayscale=True)
#     a.append(time.time() - t)
#     x = x + 1
# print('ok.png eingegrenzt: ' +  str(sum(a) / len(a)))

# x=0
# a = []
# while x < i:
#     t = time.time()
#     r = pyautogui.pixelMatchesColor(int(ench_window_x + 83),int(ench_window_y + 382), (230, 217, 190))
#     a.append(time.time() - t)
#     x = x + 1
# print(str(not r)+' Pixelmatching: ' +  str(sum(a) / len(a)))

# if pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
#     print('Speicherfehlermeldung auf dem Bildschirm - starte neu.')
#     while pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
#         pyautogui.moveTo(pyautogui.locateCenterOnScreen(path + 'pic\\OK_Error.png',grayscale=True, confidence=.88))
#         mausklick()
#         time.sleep(1)
#         mausklick()

raise_process_priority()
context = lib.interception_create_context()

lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_ALL)

stroke = ffi.new('InterceptionKeyStroke *')

while True:
    device = lib.interception_wait(context)
    if stroke.code == SCANCODE.SCANCODE_ESC:
        print('ESC')

lib.interception_destroy_context(context)