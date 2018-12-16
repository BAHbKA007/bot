#! python3
import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    while True:
        im = pyautogui.screenshot()
        x, y = pyautogui.position()
        color =  str(im.getpixel((x, y)))
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + ' Farbe: '  + color
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
