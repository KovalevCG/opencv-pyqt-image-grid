import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        # create button
        self.button = QPushButton("test button", self)
        self.button.resize(100, 30)

        # set button context menu policy
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.on_context_menu)

        # create context menu
        self.popMenu = QMenu(self)
        self.popMenu.addAction(QAction('test0', self))
        self.popMenu.addAction(QAction('test1', self))
        self.popMenu.addSeparator()
        self.popMenu.addAction(QAction('test2', self))

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.button.mapToGlobal(point))

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()