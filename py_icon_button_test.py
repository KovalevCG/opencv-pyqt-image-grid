import py_icon_button
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        layout = QVBoxLayout()
        button = py_icon_button.PyIconButton("My Button")
        layout.addWidget(button)
        self.setLayout(layout)


app = QApplication([])
window = MyWidget()
window.show()
app.exec_()