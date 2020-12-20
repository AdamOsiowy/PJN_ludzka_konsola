import sys
from win32api import GetSystemMetrics
import os.path
from PyQt5.Qt import Qt
import interface
import voice
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import queue
import threading
import os

SCREEN_SIZE = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))


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
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.click)
        self.counter = 0

        self.commands = queue.Queue()
        self.locker = threading.Lock()

        self.threadpool = QtCore.QThreadPool()
        self.worker = Worker(self.threadLoop)

        self.threadpool.start(self.worker)

        self.labelChanged.connect(self.ui.lineEdit.setText)

        self.event_stop = threading.Event()

    def click(self):
        self.ui.lineEdit.setText(voice.recognizeVoice())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            self.ui.lineEdit.setText(str(self.counter))
            self.counter += 1

    def threadLoop(self):
        while not self.event_stop.is_set():
            self.insideThread()

    def insideThread(self):
        for i in range(10):
            print(i)
            QtCore.QThread.sleep(1)
        self.event_stop.set()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.event_stop.set()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    sys.exit(app.exec_())
