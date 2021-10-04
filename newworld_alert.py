from win32 import win32gui
import win32ui
from ctypes import windll
from PIL import Image, ImageOps
import numpy as nm
import pytesseract
import cv2
import sched
import time
from playsound import playsound
import os

s = sched.scheduler(time.time, time.sleep) # Initialise scheduler for looping new world queue grab
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" # Tesseract exe location
# Get alert mp3 and ensure exists
alert_sound = os.getcwd() + "/alert.mp3"
if not os.path.isfile(alert_sound):
    print("\033[31m Alert sound not found, please make sure 'alert.mp3' is in the same directory as this script!")
    exit()


def getNewWorldPosition():
    # Get New World Screenshot - using win32gui so can grab in background
    hwnd = win32gui.FindWindow(None, 'New World')

    if hwnd == 0:
        try:
            print(
                "\033[31m New World window not found, make sure the game is open and currently queuing! Will retry in 5 seconds...")
            return
        finally:
            s.enter(5, 1, getNewWorldPosition)

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # Crop image to queue position number (on a 2560x1440 display)
    scrnshot = im.crop((1130, 650, 1440, 730))
    # Convert image to monochrome for better OCR accuracy
    scrnshot = cv2.cvtColor(nm.array(scrnshot), cv2.COLOR_BGR2GRAY)
    # Get queue number
    tesstr = pytesseract.image_to_string(scrnshot, lang='eng')
    try:
        queuenum = int(tesstr)
        print(f"Queue Position: {queuenum}")
        if queuenum < 50:
            print(
                "\033[92m Almost at end of queue, open up New World now! Press CTRL+C to exit program")
            while True:
                try:
                    playsound(alert_sound)  # Play alert sound if in queue
                except KeyboardInterrupt:
                    exit()
    except ValueError:
        print(
            "\033[93m Queue number not found, retrying in 15 seconds. Make sure you have clicked 'Play'!")

    s.enter(15, 1, getNewWorldPosition)


def main():
    s.enter(0, 1, getNewWorldPosition)
    s.run()


main()
