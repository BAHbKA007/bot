import pyautogui, win32gui, os, time, math
from interception import ffi, lib

path = str(os.path.dirname(__file__)) + '\\pic\\'
start_time = int(math.ceil(time.time()))

class SCANCODE: 
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002
    TAB = 0x0F
    MONITORPOWER = 0xF170

    F1=0x3B
    F2=0x3C
    F3=0x3D
    F4=0x3E
    F5=0x3F
    F6=0x40
    F7=0x41
    F8=0x42
    F9=0x43
    F10=0x44

win_pos = win32gui.GetWindowRect(win32gui.FindWindow(None, "Lineage II"))
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

#Party Fenster Koordinaten und Lebesanzeige Position
b = pyautogui.locateOnScreen(path+'party.png', grayscale=True)
#pyautogui.screenshot('temp.png', region=(b[0]+15,b[1]+8, 150, 1)) 

leben_x = b[0]+15 # 150 Pixel lang
leben_y = b[1]+8

def klick(key):
    context = lib.interception_create_context()

    stroke = ffi.new('InterceptionMouseStroke *')
        
    stroke.state  = key
    lib.interception_send(context, 1, stroke, 1)

    lib.interception_destroy_context(context)

def life_pix(pix):
    return pyautogui.pixelMatchesColor(int(leben_x + pix), int(leben_y), (231, 73, 132)) #(226, 58, 112)

time.sleep(5)

win32gui.MoveWindow(win32gui.FindWindow(None, "Lineage II"), 550, 0, 816, 639, True)
win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Lineage II"))

klick(SCANCODE.F10)
time.sleep(1)
klick(SCANCODE.F4)
time.sleep(0.5)
klick(SCANCODE.F5)

while True:

    klick(SCANCODE.F10)

    if not life_pix(130)
        while not life_pix(75):
            print('heal')
            klick(SCANCODE.F1)

    # Balance
    # if ( start_time - int(math.ceil(time.time())) ) % 20 == 0:
    #     print('Balance')
    #     klick(SCANCODE.F2)
    #     time.sleep(0.5)
    #     klick(SCANCODE.F10)

    # Bank
    if ( start_time - int(math.ceil(time.time())) ) % 45 == 0:
        print('Bank')
        klick(SCANCODE.F9)
        time.sleep(2)
        klick(SCANCODE.F10)

    time.sleep(0.5)
