import os
import json
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QApplication([])


class Tab(QWidget):
    def __init__(self, path, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)

        self.path = path

        self.init()

    def init(self):

        layout_v = QVBoxLayout()
        layout_h = QHBoxLayout()
        for file in os.listdir(self.path):
            btn = QPushButton(file)
            btn.clicked.connect(lambda b, file=file: self.open_file(b, file))
            layout_v.addWidget(btn)

        layout_v.addStretch(1)
        scroll = QScrollArea()
        scrollContent = QWidget()
        scrollContent.setLayout(layout_v)
        scroll.setWidget(scrollContent)
        box = QVBoxLayout()
        box.addWidget(scroll)

        self.setLayout(box)

    def open_file(self, b, file):
        os.startfile(self.path + "\\" + file)


class Tabs(QTabWidget):
    def __init__(self, width=270, height=750, title="Launcher"):
        super().__init__()

        self.width = width
        self.height = height
        self.title = title

        self.init()

    def init(self):
        with open("tabs.json") as tabs:
            tabs = json.load(tabs)

        for tab in tabs["tabs"]:
            self.x = Tab(path=tab["path"])
            self.addTab(self.x, tab["name"])

        # Window

        self.setGeometry(1000, 500, self.width, self.height)
        self.setWindowTitle(self.title)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.init()

    def init(self):
        tabs = Tabs()
        self.setCentralWidget(tabs)

    def settings(self):
        settings = QDialog(self)
        settings.setWindowTitle("Settings")
        settings.exec_()


w = Window()
w.show()

sys.exit(app.exec_())
