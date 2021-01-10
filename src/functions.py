import win32api
import win32con
import subprocess
import os
import getpass
import glob
import win32com.client
import re
import wmi
import pyautogui
import webbrowser
import pdf2image
import PyPDF2
from pywinauto import Application
import json
import urllib.request
import pafy

pathsOfApps = dict()


def findTask(order):
    d = {
        'podwyższyć': 'zwiększyć', 'zwiększyć': 'zwiększyć',
        'pomniejszyć': 'zmniejszyć', 'pozmniejszać': 'zmniejszyć', 'zredukować': 'zmniejszyć', 'obniżyć': 'zmniejszyć',
        'zniżyć': 'zmniejszyć', 'zciszyć': 'zmiejszyć', 'zmniejszyć': 'zmniejszyć',
        'wyciszyć': 'wyciszyć',
        'odtworzyć': 'puścić', 'puścić': 'puścić',
        'zapauzować': 'zatrzymać', 'wstrzymać': 'zatrzymać', 'zatrzymać': 'zatrzymać',
        'odpalić': 'uruchomić', 'włączyć': 'uruchomić', 'uruchomić': 'uruchomić',
        'otworzyć': 'otworzyć',
        'zakończyć': 'zamknąć', 'zlikwidować': 'zamknąć', 'przerwać': 'zamknąć', 'wyłączyć': 'zamknąć',
        'zamknąć': 'zamknąć',
        'cyknąć': 'zrobić', 'stworzyć': 'zrobić', 'wykonać': 'zrobić', 'zrobić': 'zrobić',
        'odszukać': 'znaleźć', 'wyszukać': 'znaleźć', 'odnaleźć': 'znaleźć', 'znaleźć': 'znaleźć',
        'przerobić': 'konwertować', 'konwertować': 'konwertować',
        'ściągnąć': 'pobrać', 'pobrać': 'pobrać'
    }
    if order not in d.keys():
        print("Command not supported!!!")
        return ''
    return d[order]


def completeTask(task_with_args: dict):
    print(f'complete task: {task_with_args}')
    order = task_with_args['order']
    args = task_with_args['args']
    supported_commands = {
        'zwiększyć': increaseVolume,
        'zmniejszyć': decreaseVolume,
        'wyciszyć': muteSound,
        'puścić': playTrack,
        'zatrzymać': pauseTrack,
        'uruchomić': runApp,
        'otworzyć': openFile,
        'zamknąć': closeApp,
        'zrobić': makeScreenshot,
        'znaleźć': find,
        'konwertować': convertFromMp4ToMp3,
        'pobrać': downloadFromYT
    }
    order = findTask(order)
    if len(order) > 0:
        supported_commands[order](args)


def increaseVolume(args):
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def decreaseVolume(args):
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def muteSound(args):
    win32api.keybd_event(win32con.VK_VOLUME_MUTE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


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
        if re.match(reg, key, re.IGNORECASE):
            subprocess.call(paths[key])
            break


def openFile(args):
    path = "../res/"
    for key in args.keys():
        if args[key] == "SUBST":
            os.startfile(path + key)


def closeApp(args):
    reg = '.?'.join(args.keys()) + '.*'
    f = wmi.WMI()
    list_of_processes = [(proc.ProcessId, proc.Name) for proc in f.Win32_Process()]
    pid = -1
    for pair in list_of_processes:
        if re.match(reg, pair[1], re.IGNORECASE):
            pid = pair[0]
            break
    if pid != -1:
        os.kill(pid, 9)


def makeScreenshot(args):
    current_dir = os.getcwd()
    os.chdir('../res')
    pngFiles = glob.glob(r'screenshot*.png')
    SCREEN_SIZE = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    max_value = 0
    if len(pngFiles) != 0:
        numbers = [int(re.search('[0-9]+', x, flags=re.MULTILINE).group()) for x in pngFiles]
        max_value = max(numbers)
    screenshot_name = "screenshot" + str(max_value + 1) + ".png"
    while os.path.exists(screenshot_name):
        i = max_value + 2
        screenshot_name = 'screenshot' + str(i) + '.png'
        i += 1
    pyautogui.screenshot(screenshot_name, SCREEN_SIZE)
    os.chdir(current_dir)


def find(args):
    in_web = False
    for key in args.keys():
        if re.match('intern', key):
            in_web = True
            args.pop(key)
        if re.match('siec', key):
            in_web = True
            args.pop(key)
        if re.match('przeglądar', key):
            in_web = True
            args.pop(key)
        if re.match('necie', key):
            in_web = True
            args.pop(key)
        if re.match('stron', key):
            in_web = True
            args.pop(key)
        if re.match('plik', key):
            args.pop(key)
        if re.match('pdf', key):
            args.pop(key)
    if in_web:
        findInWeb(args)
    else:
        findInPdfFiles(args)


def findInWeb(args):
    chrome_path = r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    url = "https://www.google.com/search?q=" + '+'.join(args.keys())
    webbrowser.get(chrome_path).open(url)


def findInPdfFiles(args):
    current_dir = os.getcwd()
    os.chdir('../res')
    pdfFiles = glob.glob('*.pdf')
    key = ' '.join(args.keys())
    pagesToDisplay = []
    for file in pdfFiles:
        pdfReader = PyPDF2.PdfFileReader(file)
        images = pdf2image.convert_from_path(file)
        for i in range(pdfReader.getNumPages()):
            page = pdfReader.getPage(i)
            content = page.extractText()
            if re.search(key, content, re.IGNORECASE):
                pagesToDisplay.append(images[i])
    for img in pagesToDisplay:
        img.show()
    os.chdir(current_dir)


def convertFromMp4ToMp3(args):
    current_dir = os.getcwd()
    os.chdir('../res')
    mp4_files = glob.glob('*.mp4')
    reg = '.?'.join(args.keys()) + '.*'
    file_name = ''
    for file in mp4_files:
        res = re.search(reg, file, re.I)
        if res:
            file_name = res.group()[:-4] + '.mp3'
    command = '..\\res\\bin\\ffmpeg.exe -hide_banner -loglevel quiet -i .\\'
    command += file_name[:-4] + '.mp4'
    command += '.webm -vn -ab 128k -ar 44100 -y .\\'
    command += file_name
    print(f'convert command: {command}')
    subprocess.call(command, shell=True)
    os.chdir(current_dir)


def downloadFromYT(args):
    app = None
    element_name = "Pasek adresu i wyszukiwania"
    video_id = ""
    api_key = "AIzaSyD_E7siJ1-4DSiqcQZxeMA90tuoTW92In8"
    try:
        app = Application(backend='uia')
        app.connect(title_re=".*Chrome.*")
    except:
        print("can't connect to chrome!")
    try:
        dlg = app.top_window()
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()
        res = re.search(r'(?<=watch\?v=).{11}|(?<=youtu.be/).{11}|(?<=y2u.be/).{11}', url, re.I)
        if res:
            video_id = res
    except:
        print("can't get link from chrome")
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    json_url = urllib.request.urlopen(api_url)
    data = json.loads(json_url.read())
    video_title = data['items'][0]['snippet']['title']
    video_title = re.sub(r'[.&#$ |/]', '', video_title)
    try:
        video = pafy.new(video_id, ydl_opts={'cookiefile': '../res/youtube.com_cookies.txt'})
        best = video.getbest(preftype='mp4')
        best.download(filepath=r'../res/' + video_title + '.mp4', quiet=True)
    except:
        print(f"can't download {video_title}")
