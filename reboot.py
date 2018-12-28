import os, time, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

neustart = 3600
start_time = time.time()

while True:
    rest = int(start_time + neustart - time.time())
    h = str(int(rest / 60 / 60))
    m = str(int(rest / 60 % 60))
    s = str(rest % 60 % 60)

    printstring = 'Neustart in: Sek: ' + str(rest) + ' | in Std: ' + h.zfill(2) + ' : ' + m.zfill(2) + ' : ' + s.zfill(2)
    print(printstring, end='')
    print('\b' * len(printstring), end='', flush=True)

    if (start_time + neustart - time.time()) < 0:
        print('Reboot PC...')
        os.system("shutdown -t 0 -r -f")
    requests.get('http://s.leichtbewaff.net/?reboot=' + printstring, verify=False)
    time.sleep(1)