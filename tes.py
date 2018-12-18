import time, pyautogui

path = 'C:\\Users\\Johann\\Desktop\\Bot\\pic\\'

print(pyautogui.locateCenterOnScreen(path + 'disc.png', region=(362, 352,50,50),grayscale=True, confidence=.9) != None)

input()
