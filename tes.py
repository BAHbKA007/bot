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

# ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
# ench_window_x = ench_window[0]
# ench_window_y = ench_window[1]

# #pyautogui.screenshot('delete.png', region=(ench_window_x + 160, ench_window_y + 382, 6, 8))

# while pyautogui.locateOnScreen(path + 'pic\\cancel.png', region=(ench_window_x + 160, ench_window_y + 382, 6, 8),grayscale=True, confidence=.99) != None:
#     print('da')

def find_pic(a, conf=.9, x=800, y=600, x_inner=0, y_inner=0):
    pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
    pyautogui.moveTo(pos)
    return pos

print(find_pic('login.png',.9,352,359,20,20))
