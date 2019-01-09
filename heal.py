import pyautogui, win32gui, os, time, math, sys
from interception import ffi, lib

path = str(os.path.dirname(__file__)) + '\\pic\\'
start_time = int(math.ceil(time.time()))
os.system("title Heal")

class SCANCODE: 
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002
    TAB = 0x0F
    SCANCODE_ESC = 0x01

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
    F11=0x45

win_pos = win32gui.GetWindowRect(win32gui.FindWindow(None, "Lineage II"))
win_pos_x = win_pos[0] + 7
win_pos_y = win_pos[1]

win32gui.MoveWindow(win32gui.FindWindow(None, "Lineage II"), 550, 0, 816, 639, True)
win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Lineage II"))

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

def mausklick():
    context = lib.interception_create_context()

    stroke = ffi.new('InterceptionMouseStroke *')
        
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    lib.interception_send(context, 11, stroke, 1)
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    lib.interception_send(context, 11,  stroke, 1)
    lib.interception_destroy_context(context)

def main():
    global win_pos_y,win_pos_x,leben_y,leben_x
    start = time.time()
    if int(time.time()) % 60 == 0:
        #Party Fenster Koordinaten und Lebesanzeige Position
        b = pyautogui.locateOnScreen(path+'party.png', grayscale=True)
        #pyautogui.screenshot('temp.png', region=(b[0]+15,b[1]+8, 150, 1)) 

        leben_x = b[0]+15 # 150 Pixel lang
        leben_y = b[1]+8

    farbe = pyautogui.pixelMatchesColor(win_pos_x + 49, win_pos_y + 76, (181, 0, 24))
    if not farbe:
        klick(SCANCODE.F8)
        time.sleep(.05)
        print('heal self ')
        klick(SCANCODE.F1)
        time.sleep(.05)

    klick(SCANCODE.F10)
    time.sleep(.05)

    farbe = pyautogui.pixelMatchesColor(int(leben_x + 75), int(leben_y), (231, 73, 132))
    if not farbe:
        klick(SCANCODE.F10)
        print('heal ')
        time.sleep(.05)
        klick(SCANCODE.F1)
        time.sleep(.05)

    if pyautogui.pixelMatchesColor(win_pos_x + 26, win_pos_y + 572, (0, 251, 0)):
        print('Balance')
        klick(SCANCODE.F2)
        time.sleep(0.6)
        klick(SCANCODE.F3)
        time.sleep(2)
        klick(SCANCODE.F3)
        time.sleep(1)
        klick(SCANCODE.F10)
        time.sleep(0.1)
        klick(SCANCODE.F10)

    # Bank
    if ( start_time - int(math.ceil(time.time())) ) % 45 == 0:
        print('Bank')
        klick(SCANCODE.F9)
        time.sleep(2)
        klick(SCANCODE.F10)

    farbe = pyautogui.pixel(int(leben_x + 75), int(leben_y) )

    if farbe == (255,255,-1):
        sys.exit(0)

    print(time.time()-start) 

klick(SCANCODE.F10)
time.sleep(1)
klick(SCANCODE.F4)
time.sleep(0.5)
klick(SCANCODE.F5)
time.sleep(0.5)
klick(SCANCODE.F6)

while True:

    main()
