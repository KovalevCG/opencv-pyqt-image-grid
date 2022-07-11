from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowTitle("My App")
        button = QPushButton("Press Me")
        button.setFixedSize(30, 30)
        self.setCentralWidget(button)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
