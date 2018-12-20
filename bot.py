import time, pyautogui, sys, requests, urllib3, traceback, win32gui, os, datetime, re
import pytesseract
from interception import ffi, lib
from PIL import Image
from skimage.io import imread

#https://github.com/tesseract-ocr/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SCANCODE:
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002

def mausklick():
    context = lib.interception_create_context()

    stroke = ffi.new('InterceptionMouseStroke *')
        
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    lib.interception_send(context, 11, stroke, 1)
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    lib.interception_send(context, 11,  stroke, 1)

datum_sql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
requests.get('http://s.leichtbewaff.net/?start='+str(datum_sql), verify=False)

def main(r):

    path = str(os.path.dirname(__file__)) + '\\'
 
    e = 0
    i = 5
    c = 0
    arc_count = 0
    v = 0.05 # 0.05 sleep auf den tasten
    ok = 0.239 # + sleep auf OK
    k = 0

    #Windows Prozesse Nach lineage 2 durhsuchen
    wins = []
    proc = []
    win32gui.EnumWindows(lambda x, y: y.append(x), wins)
    for winId in wins:
        winName = win32gui.GetWindowText(winId)
        if winName == 'Lineage II':
            proc.append(winId)

    # Fenster in Fordergrund bringen
    win32gui.SetForegroundWindow(proc[len(proc)-1])

    with open(path + "bot.run", "r") as fh:
        run = int(fh.read())

    while i != -1:
        print(str(i))
        time.sleep(1)
        i = i - 1
    
    if len(proc) > 0:
        def logIn():
            # Login: 462,443
            find_pic('login.png')
            mausklick()
            time.sleep(4)

            # Agree: 473,609
            find_pic('agree.png')
            mausklick()
            time.sleep(4)

            # OK: 517,450
            find_pic('ok.png')
            mausklick()
            time.sleep(4)

            # Start: 514,714
            find_pic('start.png')
            mausklick()
            time.sleep(10)

        win_pos = win32gui.GetWindowRect(proc[len(proc)-1])
        win_pos_x = win_pos[0] + 7
        win_pos_y = win_pos[1]

        def find_pic(a, conf=.9, x=800, y=600, x_inner=0, y_inner=0):
            pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
            pyautogui.moveTo(pos)
            return pos      
    else:
        raise RuntimeError('Keine Lineage II Prozesse gefunden')

    if find_pic('login.png') != None:
        logIn()

    def www_get(run, arc_count, discon, succes):
        requests.get('http://s.leichtbewaff.net/?run='+str(run)+'&arc='+str(arc_count)+'&discon='+str(discon) + '&succes=' + str(succes), verify=False)

    def setzen():
        pyautogui.moveTo(sit)
        mausklick()
        time.sleep(2)   

    def no_arc18er():
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
        i = len(list(temp))
        print('Anzahl gefundener Gegenstände: ' + str(i))

        if arc_count >= i:
            return True
        else:
            return False

    #logIn()

    # ews Koordinaten, Farbe + Anzahl BEWS
    ews = find_pic('ews.png',0.99)
    time.sleep(2)
    b = pyautogui.locateOnScreen(path + 'pic\\' + 'BEWS.png')

    pyautogui.screenshot('temp.png', region=(b[0],b[1], 300, 23))
    image = imread('temp.png')
    negative = 255 - image
    ews_count = int(pytesseract.image_to_string(negative)[41:].split(')')[0].replace(",","").replace(" ","").replace("(",""))

    # Enchant Fenster Koordinaten
    mausklick()
    time.sleep(1)
    ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9)
    ench_window_x = ench_window[0]
    ench_window_y = ench_window[1]

    # CP Koordinaten
    cp = 0#find_pic('cp.png',0.99)
    
    # relog Koordinaten
    relog = find_pic('relog.png',0.99)

    # relog Koordinaten
    sit = find_pic('sit.png',0.99)

    if ews != None and cp != None and relog != None and sit != None:

        if r == 0:
            setzen()
    
        try:
            while True:
                # EWS Prüfung             
                if ews_count == 0:
                    print('Keine EWS mehr (verschoben?)!')
                    break

                # Prüfen ob Disconnect Fehlermeldung auf dem Bildschirm
                if pyautogui.locateCenterOnScreen(path + 'pic\\disc.png', region=(win_pos_x + 370, win_pos_y + 330,40,40),grayscale=True, confidence=.9) != None:
                    www_get(run, arc_count, 1, 0)
                    print('Disconnected')
                    time.sleep(1)

                    if "03:30" < time.strftime("%H:%M") < "04:00":
                        print('sleep Nacht')
                        time.sleep(1800)

                    # OK: 513,463
                    find_pic('ok.png')
                    mausklick()
                    time.sleep(4)

                    while find_pic('ews.png',0.99) == None:
                        logIn()

                    setzen()

                #Spiel an?
                if run % 20 == 0:
                    if win32gui.FindWindow(None,'Lineage II') == 0:
                        print('Lineage nicht gefunden')
                        www_get(run, arc_count, 1, 0)
                        break

                # CP craft
                # if run % 2000 == 0 and run != 0:
                #     setzen()
                #     pyautogui.moveTo(cp)
                #     mausklick()
                #     time.sleep(30)
                #     setzen()
                #     time.sleep(3)

                # relog nach 2000 runs
                if run % 6000 == 0 and run != 0:
                    pyautogui.moveTo(relog)
                    mausklick()
                    time.sleep(10)

                # Echnant
                pyautogui.moveTo(ews)
                mausklick()
                time.sleep(v)

                # Arc
                pyautogui.moveTo(ench_window_x + 24 + c, ench_window_y + k + 67)
                mausklick()
                time.sleep(v)

                if no_arc18er():
                    #OK Button Enchant Fenster
                    pyautogui.moveTo(ench_window_x + 90, ench_window_y + 383)
                    mausklick()
                    time.sleep(v + ok) #0.25

                else:
                    if arc_count == 5:
                        # www_get(run, arc_count, 1, 1)
                        # print('Mehr als 6 Gegenstände 18+')
                        # break
                        c = -36
                        k = k + 36
                    if arc_count == 11:
                        www_get(run, arc_count, 1, 1)
                        print('Mehr als 6 Gegenstände 18+')
                        break

                    arc_count = arc_count + 1
                    c = c + 36

                    requests.get('http://s.leichtbewaff.net/?stat='+str(run), verify=False)
                    run = 0

                printstr = str(arc_count) + ' Arcana Mace ' + str(run) + ' Durchläufe ' + str(ews_count) + ' EWS'
                print(printstr)

                www_get(run, arc_count, 0, 0)

                #bot.run beschreiben
                with open(path + "bot.run", "w") as fh:
                    fh.write(str(run))

                run = run + 1
                ews_count = ews_count - 1

        except Exception as e:
            www_get(0, 0, 1, 0)

            with open(path + "bot.run", "w") as fh:
                fh.write(str(run))

            print("type error: " + str(e))
            print(traceback.format_exc())

            main(1)

main(0)