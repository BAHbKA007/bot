import time, pyautogui, sys, requests, urllib3, traceback, win32gui, os, datetime, re, math
import pytesseract, subprocess, psutil
from interception import ffi, lib
from PIL import Image
from skimage.io import imread

# https://github.com/tesseract-ocr/tesseract/wiki
# pip install pyautogui requests urllib3 pypiwin32 pytesseract psutil interception scipy screeninfo
# https://github.com/oblitum/interception/releases/tag/v1.0.1
# %windir%\system32\cmd.exe /K python /Users/Johann/Desktop/Bot/bot.py
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.system("title Bot")

path = str(os.path.dirname(__file__)) + '\\'
datum_sql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
requests.get('http://s.leichtbewaff.net/?start='+str(datum_sql), verify=False)
start_time = int(math.ceil(time.time()))
v = 0.05 # 0.05 sleep auf den tasten
ok = 0.3 # + sleep auf OK .239
arc_count = 0
while_count = 0
break_var = False
x_schieber = 0
y_schieber = 0
finder_count = 0
neustart = 9000 # 9000
login = 'bahbka1'
pw = '090587'
with open(path + "bot.run", "r") as fh:
    run = int(fh.read())


#               PICTURE
#
#
#
PICTURE = 'ews.png'
#
#
if PICTURE.find('w') != -1:
    max_enchant = '18.png'
else:
    max_enchant = '14.png'
#

class SCANCODE: 
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN   = 0x001
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP     = 0x002
    TAB = 0x0F
    MONITORPOWER = 0xF170

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

def discon(address):
    return not not os.system('ping %s -n 1 > NUL' % (address,))

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

def mausklick():
    context = lib.interception_create_context()

    stroke = ffi.new('InterceptionMouseStroke *')
        
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    lib.interception_send(context, 11, stroke, 1)
    stroke.state  = SCANCODE.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    lib.interception_send(context, 11,  stroke, 1)
    lib.interception_destroy_context(context)

def login_versuche(start):
    if time.time() - start > 20:
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == 'l2.bin' or proc.name() == 'l2.exe':
                print('beende L2 Prozess (login_versuche)')
                proc.kill()
                time.sleep(2)
                print('starte L2 (login_versuche)')
                time.sleep(5)
        return True
    else:
        return False

def main(r):
    global run, ok, v, y_schieber, x_schieber, finder_count, arc_count, break_var, neustart

    while True:

        e = 0
        while_count = 0
        x_schieber = 0
        y_schieber = 0
        finder_count = 0
        arc_count = 0

        if break_var:
            print('Neustart')
            break_var = False
            break

        # Windows Prozesse Nach lineage 2 durhsuchen
        proc = []
        # Auflösung holen
        desktop_size = []
        for i in pyautogui.size():
            desktop_size.append(int(i/2))


        # Speicherfehlermeldung
        if pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
            while pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
                print('Speicherfehlermeldung auf dem Bildschirm - starte neu.')
                pyautogui.moveTo(pyautogui.locateCenterOnScreen('pic\\OK_Error.png'))
                mausklick()
                time.sleep(1)
            break

        def find_pic(a, conf=.9, x=800, y=600, x_inner=0, y_inner=0):
            pos = pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x + x_inner, win_pos_y + y_inner,x,y),grayscale=True, confidence=conf)
            pyautogui.moveTo(pos)
            return pos  

        def www_get(run, arc_count, discon, succes):
            try:
                requests.get('http://s.leichtbewaff.net/?run='+str(run)+'&arc='+str(arc_count)+'&discon='+str(discon) + '&succes=' + str(succes), verify=False)
            except Exception as e:
                print("type error: " + str(e))
                print(traceback.format_exc())

        def setzen():
            pyautogui.moveTo(sit)
            mausklick()
            time.sleep(2)   

        def item_finder():
            global x_schieber, y_schieber, arc_count, run, finder_count

            finder_count = finder_count + 1
            if pyautogui.pixelMatchesColor(int(ench_window_x + 10 + x_schieber * 37), int(ench_window_y + 51 + y_schieber * 35), (16, 16, 16)):
                for proc in psutil.process_iter():
                # check whether the process name matches
                    if proc.name() == 'l2.bin' or proc.name() == 'l2.exe':
                        print('L2 Prozess beenden')
                        proc.kill()
                with open(path + "bot.run", "w") as fh:
                    fh.write(str(0))
                print('Keine Gegenstände mehr zum verbessern! Beende Spiel')        
                input()

            pyautogui.screenshot('ench_screen.png', region=(ench_window_x + 10 + x_schieber * 37, ench_window_y + 51 + y_schieber * 35, 12, 8))
            picture = Image.open("ench_screen.png")

            width, height = picture.size

            for x in range(0, width):
                for y in range(0, height):
                    current_color = picture.getpixel( (x,y) )
                    if current_color != (255,0,0):
                        picture.putpixel( (x,y), (0, 0, 0))

            picture.save("ench_screen.png")

            temp = pyautogui.locateAll(path + "pic\\" + max_enchant, "ench_screen.png", grayscale=False)
            i = len(list(temp))

            if i == 1:
                arc_count = arc_count + 1

                print(str(y_schieber) + ' Gegenstand gefunden ' + str(x_schieber))
                x_schieber = x_schieber + 1
                if x_schieber != 0 and x_schieber % 6 == 0:
                    y_schieber = y_schieber + 1
                    x_schieber = 0
                
                if run < 5 or finder_count == 1:
                    finder_count = 0
                    run = run - 1
                else:
                    requests.get('http://s.leichtbewaff.net/?stat='+str(run), verify=False)
                    run = 0
        
        def logIn():
            start = int(math.ceil(time.time()))

            while find_pic('login.png') == None:
                time.sleep(1)

            while find_pic('login.png') != None:
                # Login: 462,443
                print('login Button')
                find_pic('login.png')
                mausklick()
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('agree.png') == None:
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('agree.png') != None:
                # Agree: 473,609
                print('agree Button')
                find_pic('agree.png')
                mausklick()
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('ok.png') == None:
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('ok.png') != None:
                # OK: 517,450
                print('OK Button')
                find_pic('ok.png')
                mausklick()
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('start.png') == None:
                time.sleep(1)
                if login_versuche(start):
                    break

            while find_pic('start.png') != None:
                # Start: 514,714
                print('Start Button')
                find_pic('start.png')
                mausklick()
                time.sleep(1)
                if login_versuche(start):
                    break
                    
        if win32gui.FindWindow(None, "Lineage II") == 0:
            start = time.time()
            p = subprocess.Popen([r"C:\\Euro-PvP_Client_ru_en\\system\\l2.exe"], stdout=subprocess.PIPE)
            p.wait()

            while win32gui.FindWindow(None, "Lineage II") == 0:
                try:
                    time.sleep(5)
                    print('warte auf Programmstart')
                    if (time.time() - start) > 30:
                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'l2.bin' or proc.name() == 'l2.exe':
                                print('beende L2 Prozess')
                                proc.kill()
                                time.sleep(2)
                                print('starte L2')
                        break_var = True
                        break
                except Exception as e:
                    print("type error: " + str(e))
                    print(traceback.format_exc())
                    break_var = True
                    break

            if break_var:
                print('Neustart')
                break

            # Fenster in Fordergrund bringen
            win32gui.MoveWindow(win32gui.FindWindow(None, "Lineage II"), 550, 0, 816, 639, True)
            win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Lineage II"))
            
            anmelden(login,pw)

            win_pos = win32gui.GetWindowRect(win32gui.FindWindow(None, "Lineage II"))
            win_pos_x = win_pos[0] + 7
            win_pos_y = win_pos[1]

            logIn()
        else:
            win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Lineage II"))
            win_pos = win32gui.GetWindowRect(win32gui.FindWindow(None, "Lineage II"))
            win_pos_x = win_pos[0] + 7
            win_pos_y = win_pos[1]

        if break_var:
            print('Neustart')
            break

        start = int(math.ceil(time.time())) 
        while find_pic(PICTURE) == None:
            print('suche ews.png')
            if login_versuche(start):
                break_var = True
                break
            time.sleep(1)

        if break_var:
            print('Neustart')
            break

        # ews Koordinaten, Farbe + Anzahl BEWS
        # print('Scroll Anzahl holen.')
        ews = find_pic(PICTURE,0.99)
        # mausklick()
        # time.sleep(2)
        # b = pyautogui.locateOnScreen(path + 'pic\\' + 'BEWS.png')

        # while b == None:
        #     print('Scroll Anzahl holen.')
        #     ews = find_pic(PICTURE,0.99)
        #     time.sleep(2)
        #     b = pyautogui.locateOnScreen(path + 'pic\\' + 'BEWS.png')

        # pyautogui.screenshot('temp.png', region=(b[0],b[1], 300, 23))
        # image = imread('temp.png')
        # negative = 255 - image
        # ews_count = int(pytesseract.image_to_string(negative)[41:].split(')')[0].replace(",","").replace(" ","").replace("(",""))


        # Enchant Fenster Koordinaten
        mausklick()
        time.sleep(1)
        ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
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

            while True:             

                try:
                    while_count = while_count + 1
                    start_time_loop = time.time()

                    if ( start_time - int(math.ceil(time.time())) ) % 3600 == 0:
                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'l2.bin' or proc.name() == 'l2.exe':
                                print('L2 Prozess beenden')
                                proc.kill()
                        time.sleep(3)
                        print('L2 neustarten')
                        main(0)
                        
                    # # EWS Prüfung             
                    # if ews_count == 0:
                    #     print('Keine EWS mehr (verschoben?)!')
                    #     break_var = True
                    #     break

                    # alle 30 Sekunden
                    if ( start_time - int(math.ceil(time.time())) ) % 15 == 0:
                        print('Prüfungen: Disconnect und Spiel an')
                        #Prüfen ob Disconnect Fehlermeldung auf dem Bildschirm
                        if pyautogui.locateCenterOnScreen(path + 'pic\\disc.png', region=(win_pos_x + 258, win_pos_y + 270,40,40),grayscale=True, confidence=.9) != None:
                            www_get(run, arc_count, 1, 0)
                            print('Disconnected')
                            time.sleep(1)

                            for proc in psutil.process_iter():
                                # check whether the process name matches
                                if proc.name() == 'l2.bin' or proc.name() == 'l2.exe':
                                    print('L2 Prozess beenden')
                                    proc.kill()
                            time.sleep(3)
                            print('L2 neustarten')
                            break_var = True
                            break
                        
                        # Speicherfehlermeldung
                        if pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
                            print('Speicherfehlermeldung auf dem Bildschirm - starte neu.')
                            while pyautogui.pixelMatchesColor(desktop_size[0],desktop_size[1], (240, 240, 240)):
                                pyautogui.moveTo(pyautogui.locateCenterOnScreen('pic\\OK_Error.png'))
                                mausklick()
                                time.sleep(1)
                            break_var = True
                            break
                        
                        # Spiel an
                        if win32gui.FindWindow(None, "Lineage II") == 0:
                            print('Siel nicht gefunden!!!')
                            break_var = True
                            break
                    
                    # CP craft
                    # if run % 2000 == 0 and run != 0:
                    #     setzen()
                    #     pyautogui.moveTo(cp)
                    #     mausklick()
                    #     time.sleep(30)
                    #     setzen()
                    #     time.sleep(3)

                    # Serverrestart umgehen
                    if time.strftime("%H:%M") == "03:33":
                        print('sleep Nacht')
                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'l2.bin':
                                proc.kill()
                                print('Warte 20 Minuten auf Serverdown')
                                time.sleep(1200)
                        break_var = True
                        break

                    # Echnant
                    pyautogui.moveTo(ews)
                    mausklick()
                    time.sleep(v)

                    # Arc
                    pyautogui.moveTo(ench_window_x + 10 + x_schieber * 37 + 16, ench_window_y + 51 + y_schieber * 35 + 16)
                    mausklick()
                    time.sleep(v)

                    # Koordinaten Kontrolle
                    item_finder()

                    # alle 5 Minuten
                    if ( start_time - int(math.ceil(time.time())) ) % 300 == 0:
                        try:
                            print('Reset Koordinaten Enchant window')
                            pyautogui.moveTo(ews)
                            mausklick()
                            ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
                            ench_window_x = ench_window[0]
                            ench_window_y = ench_window[1]

                            if find_pic('login.png',.9,352,359,20,20) != None:
                                print('relog')
                                logIn()
                            else:
                                print('kein login on Screen')
                                pass
                        except Exception as e:
                            www_get(0, 0, 1, 0)

                            with open(path + "bot.run", "w") as fh:
                                fh.write(str(run))

                            print("type error: " + str(e))
                            print(traceback.format_exc())
                            break_var = True
                            break
                            
                    #OK Button Enchant Fenster
                    pyautogui.moveTo(ench_window_x + 90, ench_window_y + 383)
                    mausklick()
                    time.sleep(v + ok) #0.25
                    
                    www_get(run, arc_count, 0, 0)

                    #bot.run beschreiben
                    with open(path + "bot.run", "w") as fh:
                        fh.write(str(run))

                    run = run + 1
                    #ews_count = ews_count - 1

                    printstr = str(time.time() - start_time_loop)[0:5] + ' Laufzeit | run = ' + str(run)
                    print(printstr)

                except Exception as e:
                    www_get(0, 0, 1, 0)

                    with open(path + "bot.run", "w") as fh:
                        fh.write(str(run))

                    print("type error: " + str(e))
                    print(traceback.format_exc())
                    break_var = True
                    break
while True:
    try:
        if time.time() - start_time > 5:
            main(1)
        else:
            main(0)
    except Exception as e:
        if time.time() - start_time > 5:
            main(1)
        else:
            main(0)