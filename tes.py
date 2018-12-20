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

ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9)
ench_window_x = ench_window[0]
ench_window_y = ench_window[1]

pyautogui.locateAllOnScreen(path + 'pic\\14.png', region=(ench_window_x + 6, ench_window_y + 90, 230, 25), grayscale=False, confidence=.8)

pyautogui.screenshot('ench_screen.png', region=(ench_window_x + 10, ench_window_y + 51, 198, 43))
picture = Image.open("ench_screen.png")

width, height = picture.size

for x in range(0, width):
    for y in range(0, height):
        current_color = picture.getpixel( (x,y) )
        if current_color != (255,0,0):
            picture.putpixel( (x,y), (0, 0, 0))

picture.save("ench_screen.png")

temp = pyautogui.locateAll(path + "pic\\14.png", "ench_screen.png", grayscale=False)

print()