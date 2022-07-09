import os
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
for screen in QApplication.screens():
    screen_path = os.path.expanduser(f"~/Desktop/{screen.name()}.jpg")
    screen.grabWindow(0).save(screen_path, 'jpg')
    # grabWindow(0) means full screen
    # for area use following format; x=0, y=0, w=-1, h=-1