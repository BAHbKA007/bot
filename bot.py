import time, pyautogui, sys, requests, urllib3, traceback, win32gui, os, datetime, re, math
import pytesseract, subprocess, psutil
from interception import ffi, lib
from PIL import Image
from skimage.io import imread

#https://github.com/tesseract-ocr/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

datum_sql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
requests.get('http://s.leichtbewaff.net/?start='+str(datum_sql), verify=False)
start_time = int(math.ceil(time.time()))

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
    if time.time() - start > 120:
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == 'l2.bin':
                print('beende L2 Prozess')
                proc.kill()
                time.sleep(2)
                print('starte L2')
                main(0)

def main(r):

    path = str(os.path.dirname(__file__)) + '\\'
 
    e = 0
    c = 0
    arc_count = 0
    v = 0.05 # 0.05 sleep auf den tasten
    ok = 0.27 # + sleep auf OK .239
    k = 0
    while_count = 0



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
            main(1)

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

        if arc_count >= i:
            return True
        else:
            return False

    
    def logIn():
        start = int(math.ceil(time.time()))

        while find_pic('login.png') == None:
            time.sleep(1)
            login_versuche(start)

        while find_pic('login.png') != None:
            # Login: 462,443
            print('login Button')
            find_pic('login.png')
            mausklick()
            time.sleep(1)
            login_versuche(start)

        while find_pic('agree.png') == None:
            time.sleep(1)
            login_versuche(start)

        while find_pic('agree.png') != None:
            # Agree: 473,609
            print('agree Button')
            find_pic('agree.png')
            mausklick()
            time.sleep(1)
            login_versuche(start)

        while find_pic('ok.png') == None:
            time.sleep(1)
            login_versuche(start)

        while find_pic('ok.png') != None:
            # OK: 517,450
            print('OK Button')
            find_pic('ok.png')
            mausklick()
            time.sleep(1)
            login_versuche(start)

        while find_pic('start.png') == None:
            time.sleep(1)
            login_versuche(start)

        while find_pic('start.png') != None:
            # Start: 514,714
            print('Start Button')
            find_pic('start.png')
            mausklick()
            time.sleep(1)
            login_versuche(start)

    if len(find_proc()) == 0:
        start = time.time()
        p = subprocess.Popen([r"C:\\Euro-PvP_Client_ru_en\\system\\l2.exe"], stdout=subprocess.PIPE)
        p.wait()

        try:
            while len(find_proc()) == 0:
                time.sleep(5)
                print('warte auf Programmstart')
                if (time.time() - start) > 30:
                    for proc in psutil.process_iter():
                        # check whether the process name matches
                        if proc.name() == 'l2.bin':
                            print('beende L2 Prozess')
                            proc.kill()
                            time.sleep(2)
                            print('starte L2')
                            main(0)
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            main(1)

        # Fenster in Fordergrund bringen
        win32gui.SetForegroundWindow(find_proc()[len(find_proc())-1])

        anmelden('bahbka1','090587')

        win32gui.SetForegroundWindow(find_proc()[len(find_proc())-1])
        win_pos = win32gui.GetWindowRect(find_proc()[len(proc)-1])
        win_pos_x = win_pos[0] + 7
        win_pos_y = win_pos[1]

        logIn()
    else:
        win32gui.SetForegroundWindow(find_proc()[len(find_proc())-1])
        win_pos = win32gui.GetWindowRect(find_proc()[len(proc)-1])
        win_pos_x = win_pos[0] + 7
        win_pos_y = win_pos[1]

    with open(path + "bot.run", "r") as fh:
        run = int(fh.read())

    while find_pic('ews.png') == None:
        print('suche ews.png')
        time.sleep(1)

    # ews Koordinaten, Farbe + Anzahl BEWS
    try:
        print('Scroll Anzahl holen.')
        ews = find_pic('ews.png',0.99)
        time.sleep(2)
        b = pyautogui.locateOnScreen(path + 'pic\\' + 'BEWS.png')

        pyautogui.screenshot('temp.png', region=(b[0],b[1], 300, 23))
        image = imread('temp.png')
        negative = 255 - image
        ews_count = int(pytesseract.image_to_string(negative)[41:].split(')')[0].replace(",","").replace(" ","").replace("(",""))
    except Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())
        main(1)

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
    
        try:
            while True:
                while_count = while_count + 1
                start_time_loop = time.time()

                #EWS Prüfung             
                if ews_count == 0:
                    print('Keine EWS mehr (verschoben?)!')
                    break

                # alle 20 Durchläufe
                if ( start_time - int(math.ceil(time.time())) ) % 30 == 0:
                    print('Prüfungen: Disconnect und Spiel an')
                    #Prüfen ob Disconnect Fehlermeldung auf dem Bildschirm
                    if pyautogui.locateCenterOnScreen(path + 'pic\\disc.png', region=(win_pos_x + 258, win_pos_y + 270,40,40),grayscale=True, confidence=.9) != None:
                        www_get(run, arc_count, 1, 0)
                        print('Disconnected')
                        time.sleep(1)

                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'l2.bin':
                                print('L2 Prozess beenden')
                                proc.kill()
                        time.sleep(3)
                        print('L2 neustarten')
                        main(0)
                        
                # CP craft
                # if run % 2000 == 0 and run != 0:
                #     setzen()
                #     pyautogui.moveTo(cp)
                #     mausklick()
                #     time.sleep(30)
                #     setzen()
                #     time.sleep(3)

                # Serverrestart umgehen
                if "03:30" < time.strftime("%H:%M") < "04:00":
                    print('sleep Nacht')
                    for proc in psutil.process_iter():
                        # check whether the process name matches
                        if proc.name() == 'l2.bin':
                            proc.kill()
                            time.sleep(360)
                            print('Warte 6 Minuten auf Serverdown')
                    while discon('185.121.243.33'):
                        print('Server offline, warte ...')
                        time.sleep(10)
                    main(0)

                # relog nach 30min
                if ( start_time - int(math.ceil(time.time())) ) % 1800 == 0:
                    print('Relog')
                    pyautogui.moveTo(relog)
                    mausklick()
                    while find_pic('ews.png') == None:
                        print('suche ews.png')
                        time.sleep(1)
                    find_pic('ews.png',0.99)
                    time.sleep(1)
                    mausklick()
                    print('Reset Koordinaten Enchant window')
                    ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
                    ench_window_x = ench_window[0]
                    ench_window_y = ench_window[1]

                # Echnant
                pyautogui.moveTo(ews)
                mausklick()
                time.sleep(v)

                # Arc
                pyautogui.moveTo(ench_window_x + 24 + c, ench_window_y + k + 67)
                mausklick()
                time.sleep(v)

                # alle 100 Durchläufe
                if ( start_time - int(math.ceil(time.time())) ) % 300 == 0:
                    print('Reset Koordinaten Enchant window')
                    ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,800,600),grayscale=True, confidence=.9)
                    ench_window_x = ench_window[0]
                    ench_window_y = ench_window[1]

                    if find_pic('login.png',.9,352,359,20,20) != None:
                        print('relog')
                        logIn()
                    else:
                        print('kein login on Screen')
                        pass

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
                        c = -36
                        k = k + 36

                    if arc_count == 8:
                        #bot.run beschreiben
                        with open(path + "bot.run", "w") as fh:
                            fh.write(str(0))
                        break

                    if while_count > 20:
                        requests.get('http://s.leichtbewaff.net/?stat='+str(run), verify=False)
                        run = 0

                    arc_count = arc_count + 1
                    c = c + 36

                www_get(run, arc_count, 0, 0)

                #bot.run beschreiben
                with open(path + "bot.run", "w") as fh:
                    fh.write(str(run))

                printstr = str(ews_count) + ' EWS || ' + str(time.time() - start_time_loop) + 's Laufzeit || run = ' + str(run)
                print(printstr)

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