from PyQt5 import QtWidgets

import sys

# QtCore
# Qt

# class ImageLabel(QtWidgets.QLabel):
#     def __init__(self):
#         super(ImageLabel, self).__init__()


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget(windowTitle = "My Window")
window.show()

app.exec()

