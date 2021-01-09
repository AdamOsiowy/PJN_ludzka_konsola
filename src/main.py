import sys
from win32api import GetSystemMetrics
import os.path
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import queue
import threading
import os
import interface
import voice
import functions
import text_processing

SCREEN_SIZE = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))


# doc1 = 'wyłącz Spotify'
# doc2 = 'zmniejsz głośność odtwarzacza muzyki'
# doc3 = 'wyszukaj w internecie informacje o drugiej wojnie światowej'
# doc4 = 'zrób zrzut ekranu i zapisz go jako screenshot1'
# doc5 = 'zapisać zapisz'

class Worker(QtCore.QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn
        self.originating_PID = os.getpid()
        self._running = True

    @QtCore.pyqtSlot()
    def run(self):
        self.fn()


class MyWindow(QMainWindow):
    labelChanged = QtCore.pyqtSignal(str)

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.commands = queue.Queue()

        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(300, 125)

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../res/console.ico"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.locker = threading.Lock()
        self.stop_event = threading.Event()
        self.threadPool = QtCore.QThreadPool()
        self.workerMainThread = Worker(self.mainThread)
        self.threadPool.start(self.workerMainThread)

        self.ui.pushButton.clicked.connect(self.buttonClick)
        self.labelChanged.connect(self.ui.lineEdit.setText)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.commands.put('qqqq')  # to refresh main Thread while
        self.stop_event.set()

    def focusOutEvent(self, event):
        self.setFocus(True)
        self.activateWindow()
        self.raise_()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.closeEvent(event)

    def mainThread(self):
        while not self.stop_event.is_set():
            c = 'Uruchom Visual Studio Code'
            tokens = text_processing.tokenize(c)
            print(tokens)
            print(text_processing.tagPartOfSpeech(tokens))
            command = self.commands.get()
            if command == 'qqqq':
                continue
            self.insideMainThread(command)
            self.commands.task_done()

    def insideMainThread(self, command):
        command = command.lower()
        task = text_processing.getTaskAndArgs(command)
        functions.completeTask(task)

    def buttonClick(self):
        self.labelChanged.emit('')
        self.ui.pushButton.setDisabled(True)
        command = voice.recognizeVoice()
        self.commands.put(command)
        self.labelChanged.emit(command)
        self.ui.pushButton.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    sys.exit(app.exec_())
