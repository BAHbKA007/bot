import time, pyautogui, win32gui, os

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

print(find_pic('ews.png',0.9,30,30,380,710))

input()
