import time, pyautogui, sys, requests, urllib3, traceback, win32gui
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(r):
    win_pos = win32gui.GetWindowRect(win32gui.FindWindow(None,'Lineage II'))
    win_pos_x = win_pos[0] + 7
    win_pos_y = win_pos[1]

    path = 'C:\\Users\\Johann\\Desktop\\Bot\\'

    e = 0
    i = 5
    c = 0
    arc_count = 0
    v = 0 #sleep auf den tasten

    with open(path + "bot.run", "r") as fh:
        run = int(fh.read())

    while i != -1:
        print(str(i), end='')
        print('\b' * len(str(i)), end='', flush=True)
        time.sleep(1)
        i = i - 1

    def www_get(run, arc_count, discon, succes):
        requests.get('http://s.leichtbewaff.net/?run='+str(run)+'&arc='+str(arc_count)+'&discon='+str(discon) + '&succes=' + str(succes), verify=False)

    def setzen():
        pyautogui.moveTo(win_pos_x + 660, win_pos_y + 680)
        time.sleep(0.5)   

    def find_pic(a):
        pyautogui.moveTo(pyautogui.locateCenterOnScreen('C:\\Users\\Johann\\Desktop\\Bot\\pic\\' + a, region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9))


    if r == 0:
        setzen()

    # Enchant Fenster Koordinaten
    if pyautogui.locateCenterOnScreen('C:\\Users\\Johann\\Desktop\\Bot\\pic\\ews.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9) != None:
        pyautogui.moveTo(win_pos_x + 396, win_pos_y + 729)
        time.sleep(1)
        ench_window = pyautogui.locateOnScreen(path + 'pic\\enchantwindow.png', region=(win_pos_x, win_pos_y,1024,768),grayscale=True, confidence=.9)
        ench_window_x = ench_window[0]
        ench_window_y = ench_window[1]
    
    def no_arc18er():
        arc18 = pyautogui.locateCenterOnScreen(path+'pic\\18er.png',region=(ench_window_x + 10 + c, ench_window_y + 48,15,15))
        if arc18 != None:
            return False
        else:
            return True

    try:
        while True:
            # Auf Enchant springen
            pyautogui.moveTo(win_pos_x + 396, win_pos_y + 729)

            # Prüfen ob Disconnect Fehlermeldung auf dem Bildschirm
            if pyautogui.pixelMatchesColor(win_pos_x + 382, win_pos_y + 364, (239, 239, 181)):
                www_get(run, arc_count, 1, 0)
                print('Disconnected')
                time.sleep(5)

                if "03:30" < time.strftime("%H:%M") < "04:00":
                    print('sleep Nacht')
                    time.sleep(3600)
        
                # OK: 513,463
                find_pic('ok.png')
                time.sleep(4)

                # Login: 462,443
                find_pic('login.png')
                time.sleep(2)

                # Agree: 473,609
                find_pic('agree.png')
                time.sleep(2)

                # OK: 517,450
                find_pic('ok.png')
                time.sleep(3)

                # Start: 514,714
                find_pic('start.png')
                time.sleep(5)

            # Prüfe BWS und Spiel an?
            if find_pic('ews.png') == None:
                if win32gui.FindWindow(None,'Lineage II') == 0:
                    print('Keine EWS?')
                    www_get(run, arc_count, 1, 0)
                    break

            # CP craft
            if run % 2000 == 0:
                setzen()
                pyautogui.moveTo(win_pos_x + 396, win_pos_y + 683)
                time.sleep(30)
                setzen()
                pyautogui.moveTo(win_pos_x + 396, win_pos_y + 729)
                time.sleep(3)

            # relog nach 2000 runs
            if run % 6000 == 0:
                pyautogui.moveTo(win_pos_x + 623, win_pos_y + 680)
                time.sleep(0.2)
                pyautogui.moveTo(win_pos_x + 396, win_pos_y + 729)
                time.sleep(8)

            # Echnant
            pyautogui.moveTo(win_pos_x + 396, win_pos_y + 729)
            time.sleep(0.165 + v) # 0.16

            # Arc
            pyautogui.moveTo(ench_window_x + 24 + c, ench_window_y + 67)
            time.sleep(0.18 + v) #0.2

            if no_arc18er():
                #OK Button Enchant Fenster
                pyautogui.moveTo(ench_window_x + 90, ench_window_y + 383)
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