import subprocess, time, win32gui, datetime, os

path = str(os.path.dirname(__file__)) + '\\'
while True:
    zeit = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    if win32gui.FindWindow(None, "Administrator:  Bot") == 0:
        print(zeit + ' | Starte Bot')
        subprocess.call("start /wait python " + path + "bot.py" , shell=True)
    else:
        continue

    time.sleep(10)