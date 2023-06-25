import wmi
import webbrowser
import ctypes
import subprocess
import keyboard
import pyautogui
import psutil
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pyautogui.FAILSAFE = False


async def control_volume(percent):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    new_volume = min(percent / 100.0, 1.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


async def lock_screen():
    ctypes.windll.user32.LockWorkStation()


async def play_youtube_video(youtube_url):
    webbrowser.open(youtube_url)


async def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("s.png")


async def delete_all():
    pyautogui.click()
    keyboard.press("ctrl")
    keyboard.press("a")
    keyboard.release("a")
    keyboard.release("ctrl")
    pyautogui.press("backspace")


async def brightness(lvl):
    c = wmi.WMI(namespace="wmi")
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(lvl, 0)


def open_application(application_path):
    subprocess.Popen(application_path)

def check_battery():
    return psutil.sensors_battery().percent

