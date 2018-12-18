import time, pyautogui, sys, requests, urllib3, traceback, win32gui, os, datetime
from interception import ffi, lib
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
    v = 0 #sleep auf den tasten

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
        print(str(i), end='')
        print('\b' * len(str(i)), end='', flush=True)
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

        def find_pic(a):
            pyautogui.moveTo(pyautogui.locateCenterOnScreen(path + 'pic\\' + a, region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9))
        
        logIn()
        
    else:
        raise RuntimeError('Keine Lineage II Prozesse gefunden')

    def www_get(run, arc_count, discon, succes):
        requests.get('http://s.leichtbewaff.net/?run='+str(run)+'&arc='+str(arc_count)+'&discon='+str(discon) + '&succes=' + str(succes), verify=False)

    def setzen():
        find_pic('sit.png')
        mausklick()
        time.sleep(2)   

    def no_arc18er():
        arc18 = pyautogui.locateCenterOnScreen(path+'pic\\16er.png',region=(ench_window_x + 10 + c, ench_window_y + 48,15,15))
        if arc18 != None:
            return False
        else:
            return True

    if r == 0:
        setzen()

    # Enchant Fenster Koordinaten
    if pyautogui.locateCenterOnScreen(path + 'pic\\ews.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9) != None:
        find_pic('ews.png')
        mausklick()
        time.sleep(1)
        ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9)
        ench_window_x = ench_window[0]
        ench_window_y = ench_window[1]
    
    try:
        while True:
            # Prüfen ob Disconnect Fehlermeldung auf dem Bildschirm
            if pyautogui.locateCenterOnScreen(path + 'pic\\disc.png', region=(362, 352,50,50),grayscale=True, confidence=.9) != None:
                www_get(run, arc_count, 1, 0)
                print('Disconnected')
                time.sleep(5)

                if "03:30" < time.strftime("%H:%M") < "04:00":
                    print('sleep Nacht')
                    time.sleep(3600)

                # OK: 513,463
                find_pic('ok.png')
                mausklick()
                time.sleep(4)

                logIn()
                setzen()
            # Prüfe BWS und Spiel an?
            if pyautogui.locateCenterOnScreen(path + 'pic\\ews.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9) == None:
                if win32gui.FindWindow(None,'Lineage II') == 0:
                    print('Keine EWS?')
                    www_get(run, arc_count, 1, 0)
                    break

            # CP craft
            if run % 2000 == 0:
                setzen()
                find_pic('cp.png')
                mausklick()
                time.sleep(30)
                setzen()
                time.sleep(3)

            # relog nach 2000 runs
            if run % 6000 == 0:
                find_pic('relog.png')
                mausklick()
                time.sleep(10)

            # Echnant
            find_pic('ews.png')
            mausklick()
            time.sleep(0.165 + v) # 0.16

            # Arc
            pyautogui.moveTo(ench_window_x + 24 + c, ench_window_y + 67)
            mausklick()
            time.sleep(0.18 + v) #0.2

            if no_arc18er():
                #OK Button Enchant Fenster
                pyautogui.moveTo(ench_window_x + 90, ench_window_y + 383)
                mausklick()
                time.sleep(0.09 + v) #0.16

            else:
                if arc_count >= 5:
                    www_get(run, arc_count, 1, 1)
                    print('Mehr als 6 Gegenstände 18+')
                    break
                arc_count = arc_count + 1
                c = c + 36

                requests.get('http://s.leichtbewaff.net/?stat='+str(run), verify=False)
                run = 0

            printstr = str(arc_count) + ' Arcana Mace ' + str(run) + ' Durchläufe'
            print(printstr, end='')
            print('\b' * len(printstr), end='', flush=True)

            www_get(run, arc_count, 0, 0)

            #bot.run beschreiben
            with open(path + "bot.run", "w") as fh:
                fh.write(str(run))

            run = run + 1

    except Exception as e:
        www_get(0, 0, 1, 0)

        with open(path + "bot.run", "w") as fh:
            fh.write(str(run))

        print("type error: " + str(e))
        print(traceback.format_exc())

        main(1)

main(0)