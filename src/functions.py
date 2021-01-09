import sys
import win32api
import win32con
import winreg
import subprocess
import os
import pathlib
import winshell
import getpass
import glob
import win32com.client
import re

pathsOfApps = dict()


def findTask(order):
    d = {'uruchomić': 'uruchomić', 'odpalić': 'uruchomić', 'zrobić': 'zrobić', 'puścić': 'puścić',
         'zatrzymać': 'zatrzymać', 'wyszukać': 'wyszukać', 'znaleźć': 'wyszukać', 'otworzyć': 'otworzyć',
         'zmniejszyć': 'zmniejszyć', 'zwiększyć': 'zwiększyć', 'cyknąć': 'zrobić'}
    return d[order]


def completeTask(task_with_args: dict):
    supported_commands = {
        'uruchomić': runApp, 'zmniejszyć': decreaseVolume, 'zwiększyć': increaseVolume,
        'puścić': playTrack, 'zatrzymać': pauseTrack
    }
    print(f'complete task: {task_with_args}')
    order = task_with_args['order']
    args = task_with_args['args']
    if order in supported_commands.keys():
        supported_commands[order](args)
    else:
        print('command not recognized')


def increaseVolume(args):
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def decreaseVolume(args):
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def playTrack(args):
    if 'następny' in args.keys():
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    elif 'poprzedni' in args.keys():
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    else:
        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def pauseTrack(args):
    win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def getListOfApps():
    global pathsOfApps
    if len(pathsOfApps) == 0:
        shell = win32com.client.Dispatch("WScript.Shell")
        current_directory = os.getcwd()
        username = getpass.getuser()
        locations = ["C:/Users/" + username + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
                     "C:/ProgramData/Microsoft/Windows/Start Menu/Programs", "C:/Program Files/WindowsApps"]
        for location in locations:
            os.chdir(location)
            lnk_files = glob.glob('./**/*.lnk', recursive=True)
            exe_files = glob.glob('./**/*.exe', recursive=True)
            for i in exe_files:
                target = location + i[1:]
                target = re.sub(r'[\|\\]', '/', target)
                pathsOfApps.update({target.split('/')[-1][:-4].lower(): target})
            for i in lnk_files:
                shortcut = shell.CreateShortCut(i)
                target = shortcut.Targetpath
                if target.endswith(".exe"):
                    target = re.sub(r'[\|\\]', '/', target)
                    pathsOfApps.update({target.split('/')[-1][:-4].lower(): target})
        os.chdir(current_directory)
        return pathsOfApps
    else:
        return pathsOfApps


def runApp(args):
    print(f'runApp args: {args}')
    paths = getListOfApps()
    print(paths)
    paths_keys = paths.keys()
    reg = '.?'.join(args.keys()) + '.*'
    for key in paths_keys:
        if re.match(reg, key):
            subprocess.call(paths[key])


def openFile(args):
    path = "../res/"
    for key in args.keys():
        if args[key] == "SUBST":
            os.startfile(path + key)
