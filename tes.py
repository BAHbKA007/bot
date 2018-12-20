import time, pyautogui, win32gui, os, re
from PIL import Image

wins = []
proc = []

path = str(os.path.dirname(__file__)) + '\\'

win32gui.EnumWindows(lambda x, y: y.append(x), wins)
for winId in wins:
    winName = win32gui.GetWindowText(winId)
    if winName == 'Lineage II':
        proc.append(winId)

win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

# ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9)
# ench_window_x = ench_window[0]
# ench_window_y = ench_window[1]

def find_pic(a, conf=.9, x=1024, y=768, x_inner=0, y_inner=0):
    pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
    pyautogui.moveTo(pos)
    return pos
ews = find_pic('ews.png')
x,y = ews
r,g,b = pyautogui.pixel( int(x), int(y) )
print(pyautogui.pixelMatchesColor(int(x), int(y), ( int(r), int(g), int(b) ) ) )