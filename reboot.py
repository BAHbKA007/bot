import os, time
neustart = 9000
start_time = time.time()

while True:
    rest = int(start_time + neustart - time.time())
    h = str(int(rest / 60 / 60))
    m = str(int(rest / 60 % 60))
    s = str(rest % 60 % 60)

    printstring = ' | Neustart in: Sek: ' + str(rest) + ' | in Std: ' + h.zfill(2) + ' : ' + m.zfill(2) + ' : ' + s.zfill(2)
    print(printstring, end='')
    print('\b' * len(printstring), end='', flush=True)

    if (start_time + neustart - time.time()) < 0:
        print('Reboot PC...')
        os.system("shutdown -t 0 -r -f")

    time.sleep(1)