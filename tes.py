import time, pyautogui, win32gui, os, re, math, subprocess, psutil
from PIL import Image,ImageGrab
from interception import ffi, lib

# wins = []
# proc = []
# win32gui.EnumWindows(lambda x, y: y.append(x), wins)
# for winId in wins:
#     winName = win32gui.GetWindowText(winId)
#     if winName == 'Lineage II':
#         proc.append(winId)

# path = str(os.path.dirname(__file__)) + '\\'
# win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
# win_pos_x = win_pos[0] + 7
# win_pos_y = win_pos[1]

# ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
# ench_window_x = ench_window[0]
# ench_window_y = ench_window[1]

# #pyautogui.screenshot('delete.png', region=(ench_window_x + 160, ench_window_y + 382, 6, 8))

# while pyautogui.locateOnScreen(path + 'pic\\cancel.png', region=(ench_window_x + 160, ench_window_y + 382, 6, 8),grayscale=True, confidence=.99) != None:
#     print('da')

class SCANCODE:
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002
    TAB = 0x0F

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

#Windows Prozesse Nach lineage 2 durhsuchen
wins = []
proc = []

def find_proc():
    win32gui.EnumWindows(lambda x, y: y.append(x), wins)
    for winId in wins:
        winName = win32gui.GetWindowText(winId)
        if winName == 'Lineage II':
            proc.append(winId)
    return proc

# Fenster in Fordergrund bringen
#win32gui.SetForegroundWindow(proc[len(proc)-1])


print(len(find_proc()))
