from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import sys
import os
import ctypes
from datetime import date

# ##############################
#  CLASS ImageLabel
# ##############################
class ImageLabel(QtWidgets.QLabel):

    def __init__(self):
        super(ImageLabel, self).__init__()
        # self.setContentsMargins(0,0,0,0)
        # self.setFixedSize(285, 285)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n or Take a Screenshot \n\n")
        self.setScaledContents(True)
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
            }
        ''')
        self.setAcceptDrops(True)
        self.file_path = ""
        self.setScaledContents(False)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        # self.setAutoFillBackground(True)

    # Right Mouse Button Pressed on Image (QLabel)
    def contextMenuEvent(self, event):
        global img_path_1, img_path_2, img_path_3, img_path_4, default_image_path
        context_menu = QMenu(self)
        swap_horizontally = context_menu.addAction("⇿ Swap Images Horizontally")
        swap_vertically = context_menu.addAction(" ↕ Swap Images Vertically")
        swap_diagonally = context_menu.addAction("◇ Swap Images Diagonally")
        remove = context_menu.addAction("Remove Image")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        # Clear Image
        if action == remove:
            self.setText("\n\n Drop Image Here \n\n or Take a Screenshot \n\n")
            self.file_path = ""
            self.assignImagePath(self.objectName(), default_image_path)

        # Swap Images Horizontally
        if action == swap_horizontally:
            # If first row
            if (self.objectName() == "photoViewer_01") or (self.objectName() == "photoViewer_02"):
                self.swapImages(window.photoViewer_01, window.photoViewer_02)
            # If second row
            else:
                self.swapImages(window.photoViewer_03, window.photoViewer_04)

        # Swap Images Vertically
        if action == swap_vertically:
            # If first column
            if (self.objectName() == "photoViewer_01") or (self.objectName() == "photoViewer_03"):
                self.swapImages(window.photoViewer_01, window.photoViewer_03)
            # Second column
            else:
                self.swapImages(window.photoViewer_02, window.photoViewer_04)

        # Swap Images Diagonally
        if action == swap_diagonally:
            if (self.objectName() == "photoViewer_01") or (self.objectName() == "photoViewer_04"):
                self.swapImages(window.photoViewer_01, window.photoViewer_04)
            else:
                self.swapImages(window.photoViewer_02, window.photoViewer_03)

    # Swap 2 provided images
    def swapImages(self, photo_viewer1, photo_viewer2):
        global img_path_1, img_path_2, img_path_3, img_path_4
        path1 = photo_viewer1.file_path
        path2 = photo_viewer2.file_path
        if path1 == "":
            photo_viewer2.file_path = ""
            photo_viewer2.setText("\n\n Drop Image Here \n\n or Take a Screenshot \n\n")
            self.assignImagePath(photo_viewer2.objectName(), default_image_path)
        else:
            photo_viewer2.file_path = path1
            self.assignImagePath(photo_viewer2.objectName(), path1)
            icon = QtGui.QPixmap(path1)
            photo_viewer2.setPixmap(
                icon.scaled(photo_viewer2.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                            QtCore.Qt.SmoothTransformation))
            photo_viewer2.setAlignment(QtCore.Qt.AlignCenter)
        if path2 == "":
            photo_viewer1.file_path = ""
            photo_viewer1.setText("\n\n Drop Image Here \n\n or Take a Screenshot \n\n")
            self.assignImagePath(photo_viewer1.objectName(), default_image_path)
        else:
            photo_viewer1.file_path = path2
            self.assignImagePath(photo_viewer1.objectName(), path2)
            icon = QtGui.QPixmap(path2)
            photo_viewer1.setPixmap(
                icon.scaled(photo_viewer1.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                            QtCore.Qt.SmoothTransformation))
            photo_viewer1.setAlignment(QtCore.Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)
            event.accept()
        else:
            event.ignore()

    # Put Image on QLabel
    def set_image(self, file_path):
        global img_path_1, img_path_2, img_path_3, img_path_4
        icon = QtGui.QPixmap(file_path)
        self.setPixmap(icon.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.assignImagePath(self.objectName(), file_path)

    # Set "img_path_n" Global Variable
    def assignImagePath(self, obj_name, path):
        global img_path_1, img_path_2, img_path_3, img_path_4
        if obj_name == "photoViewer_01":
            img_path_1 = path
        if obj_name == "photoViewer_02":
            img_path_2 = path
        if obj_name == "photoViewer_03":
            img_path_3 = path
        if obj_name == "photoViewer_04":
            img_path_4 = path




# ##############################
#  CLASS MainWindow
# ##############################
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(430, 520)
        # self.setGeometry(300, 200, 530, 500)
        self.setWindowTitle("Image Grid v." + version + "   (lecense: Ocellus Studio)")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Widgets
        self.photoViewer_01 = ImageLabel()
        self.photoViewer_01.setObjectName("photoViewer_01")
        self.photoViewer_02 = ImageLabel()
        self.photoViewer_02.setObjectName("photoViewer_02")
        self.photoViewer_03 = ImageLabel()
        self.photoViewer_03.setObjectName("photoViewer_03")
        self.photoViewer_04 = ImageLabel()
        self.photoViewer_04.setObjectName("photoViewer_04")

        # Screen Buttons Creation
        self.screen_btn1 = QtWidgets.QPushButton("  Screenshot")
        self.screen_btn1.setToolTip("Screenshot of the first monitor")
        self.screen_btn1.setIcon(QtGui.QIcon('img\monitor_1.png'))
        self.screen_btn1_2 = QtWidgets.QPushButton()
        self.screen_btn1_2.setMaximumWidth(28)
        self.screen_btn1_2.setToolTip("Screenshot of second monitor")
        self.screen_btn1_2.setIcon(QtGui.QIcon('img\monitor_2.png'))
        self.screen_btn1_3 = QtWidgets.QPushButton()
        self.screen_btn1_3.setMaximumWidth(28)
        self.screen_btn1_3.setToolTip("Screenshot of third monitor")
        self.screen_btn1_3.setIcon(QtGui.QIcon('img\monitor_3.png'))
        # Screen Buttons Layout
        self.screen_btn1_layout = QHBoxLayout()
        self.screen_btn1_layout.setSpacing(0)
        self.screen_btn1_layout.addWidget(self.screen_btn1)
        if len(QApplication.screens()) > 1:
            self.screen_btn1_layout.addWidget(self.screen_btn1_2)
        if len(QApplication.screens()) > 2:
            self.screen_btn1_layout.addWidget(self.screen_btn1_3)

        self.screen_btn2 = QtWidgets.QPushButton("  Screenshot")
        self.screen_btn2.setIcon(QtGui.QIcon('img\monitor_1.png'))
        self.screen_btn2_2 = QtWidgets.QPushButton()
        self.screen_btn2_2.setMaximumWidth(28)
        self.screen_btn2_2.setIcon(QtGui.QIcon('img\monitor_2.png'))
        self.screen_btn2_3 = QtWidgets.QPushButton()
        self.screen_btn2_3.setMaximumWidth(28)
        self.screen_btn2_3.setIcon(QtGui.QIcon('img\monitor_3.png'))
        # Screen Buttons Layout
        self.screen_btn2_layout = QHBoxLayout()
        self.screen_btn2_layout.setSpacing(0)
        self.screen_btn2_layout.addWidget(self.screen_btn2)
        if len(QApplication.screens()) > 1:
            self.screen_btn2_layout.addWidget(self.screen_btn2_2)
        if len(QApplication.screens()) > 2:
            self.screen_btn2_layout.addWidget(self.screen_btn2_3)

        self.screen_btn3 = QtWidgets.QPushButton("  Screenshot")
        self.screen_btn3.setIcon(QtGui.QIcon('img\monitor_1.png'))
        self.screen_btn3_2 = QtWidgets.QPushButton("")
        self.screen_btn3_2.setMaximumWidth(28)
        self.screen_btn3_2.setIcon(QtGui.QIcon('img\monitor_2.png'))
        self.screen_btn3_3 = QtWidgets.QPushButton()
        self.screen_btn3_3.setMaximumWidth(28)
        self.screen_btn3_3.setIcon(QtGui.QIcon('img\monitor_3.png'))
        # Screen Buttons Layout
        self.screen_btn3_layout = QHBoxLayout()
        self.screen_btn3_layout.setSpacing(0)
        self.screen_btn3_layout.addWidget(self.screen_btn3)
        if len(QApplication.screens()) > 1:
            self.screen_btn3_layout.addWidget(self.screen_btn3_2)
        if len(QApplication.screens()) > 2:
            self.screen_btn3_layout.addWidget(self.screen_btn3_3)

        self.screen_btn4 = QtWidgets.QPushButton("  Screenshot")
        self.screen_btn4.setIcon(QtGui.QIcon('img\monitor_1.png'))
        self.screen_btn4_2 = QtWidgets.QPushButton()
        self.screen_btn4_2.setMaximumWidth(28)
        self.screen_btn4_2.setIcon(QtGui.QIcon('img\monitor_2.png'))
        self.screen_btn4_3 = QtWidgets.QPushButton()
        self.screen_btn4_3.setMaximumWidth(28)
        self.screen_btn4_3.setIcon(QtGui.QIcon('img\monitor_3.png'))
        # Screen Buttons Layout
        self.screen_btn4_layout = QHBoxLayout()
        self.screen_btn4_layout.setSpacing(0)
        self.screen_btn4_layout.addWidget(self.screen_btn4)
        if len(QApplication.screens()) > 1:
            self.screen_btn4_layout.addWidget(self.screen_btn4_2)
        if len(QApplication.screens()) > 2:
            self.screen_btn4_layout.addWidget(self.screen_btn4_3)

        self.line_menu = QtWidgets.QFrame()
        self.line_menu.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menu.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.transfer_button = QtWidgets.QPushButton("Edit")
        self.transfer_button.setFixedHeight(50)
        self.save_as_button = QtWidgets.QPushButton("Save As")
        self.save_as_button.setFixedHeight(50)
        self.save_as_button.setEnabled(False)
        self.save_as_button.setToolTip("Please use the 'Edit' button to combine an images before save them")
        self.exit_button = QtWidgets.QPushButton("Exit Editor")

        # # Tooltips
        # self.screen_btn1.setToolTip("Right Click - Select Monitor")

        # OpenCV
        self.opencv = Opencv()

        # Button connect
        self.transfer_button.clicked.connect(self.start_opencv)
        self.save_as_button.clicked.connect(self.save_file_dialog)
        self.exit_button.clicked.connect(self.close_opencv)

        self.screen_btn1.clicked.connect(lambda: self.hide_me_for_screenshot(1, 0))
        self.screen_btn1_2.clicked.connect(lambda: self.hide_me_for_screenshot(1, 1))
        self.screen_btn1_3.clicked.connect(lambda: self.hide_me_for_screenshot(1, 2))
        self.screen_btn2.clicked.connect(lambda: self.hide_me_for_screenshot(2, 0))
        self.screen_btn2_2.clicked.connect(lambda: self.hide_me_for_screenshot(2, 1))
        self.screen_btn2_3.clicked.connect(lambda: self.hide_me_for_screenshot(2, 2))
        self.screen_btn3.clicked.connect(lambda: self.hide_me_for_screenshot(3, 0))
        self.screen_btn3_2.clicked.connect(lambda: self.hide_me_for_screenshot(3, 1))
        self.screen_btn3_3.clicked.connect(lambda: self.hide_me_for_screenshot(3, 2))
        self.screen_btn4.clicked.connect(lambda: self.hide_me_for_screenshot(4, 0))
        self.screen_btn4_2.clicked.connect(lambda: self.hide_me_for_screenshot(4, 1))
        self.screen_btn4_3.clicked.connect(lambda: self.hide_me_for_screenshot(4, 2))

        # Layout
        self.main_layout = QtWidgets.QGridLayout()

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setStyleSheet("QMenuBar {"
                                        "background-color: #f0f0f0;"
                                       "}"
                            "QMenuBar::item {"
                                        "background: #f0f0f0;"
                                        "}")
        # --- File Menu ---
        file_menu = self.menu_bar.addMenu("File")
        # Save As
        self.save_as_action = QAction('Save As', self)
        file_menu.addAction(self.save_as_action)
        self.save_as_action.triggered.connect(self.save_file_dialog)
        self.save_as_action.setEnabled(False)
        # Save As for Zenly Project
        self.save_as_action_zenly = QAction('Save As for Zenly', self)
        file_menu.addAction(self.save_as_action_zenly)
        self.save_as_action_zenly.triggered.connect(self.save_file_dialog_zenly)
        self.save_as_action_zenly.setEnabled(False)
        # save_as_action.setShortcut('Ctrl+S')
        # Exit
        exit_action = QAction('Exit', self)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)
        # exit_action.setShortcut('Ctrl+Q')
        # --- Help Menu ---
        help_menu = self.menu_bar.addMenu("Help")
        # About
        about_action = QAction('About', self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about)

        # Show menu
        self.menu_bar.show()

        # Logo
        # self.logo = QLabel(self)
        # self.logo.setPixmap(QtGui.QPixmap("img/ocellus_blue.png").scaled(30,30))
        # self.logo.scaled(60, 60)
        # self.logo.show()


        # Main Layout
        self.main_layout.addWidget(self.menu_bar, 0, 0, 1, 2)
        self.main_layout.addWidget(self.line_menu, 1, 0, 1, 2)

        self.main_layout.addWidget(self.photoViewer_01, 2, 0)
        self.main_layout.addLayout(self.screen_btn1_layout, 3, 0, 1, 1, alignment=QtCore.Qt.AlignBottom)

        self.main_layout.addWidget(self.photoViewer_02, 2, 1)
        self.main_layout.addLayout(self.screen_btn2_layout, 3, 1, alignment=QtCore.Qt.AlignBottom)

        self.main_layout.addWidget(self.photoViewer_03, 4, 0)
        self.main_layout.addLayout(self.screen_btn3_layout, 5, 0, alignment=QtCore.Qt.AlignBottom)

        self.main_layout.addWidget(self.photoViewer_04, 4, 1)
        self.main_layout.addLayout(self.screen_btn4_layout, 5, 1, alignment=QtCore.Qt.AlignBottom)

        self.main_layout.addWidget(self.line, 6, 0, 1, 2)
        self.main_layout.addWidget(self.transfer_button, 7, 0, 1, 1)
        self.main_layout.addWidget(self.save_as_button, 7, 1, 1, 1)
        # self.main_layout.addWidget(self.exit_button, 8, 1, 1, 1)
        # main_layout.addWidget(self.label_about)

        self.setLayout(self.main_layout)


    def show_about(self):
        print("show about")
        about_box = QMessageBox()
        # about_box.setFixedSize(500, 200);
        about_box.setIcon(QMessageBox.Information)
        about_box.setWindowTitle("About")
        about_box.setText("  Image Grid v" + version + "   \n\n           2022         \n by Alexander Kovalev \n kovalev.cg@gmail.com")
        about_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # b1 = QPushButton("ok", d)
        # b1.move(50, 50)
        # msg_box.setWindowTitle("Dialog")
        # msg_box.setWindowModality(Qt.ApplicationModal)
        about_box.exec_()

    def closeEvent(self, event):
        self.close_opencv()
        event.accept()

        # quit_msg = "Are you sure you want to exit the program?"
        # reply = QMessageBox.question(self, 'Message',
        #                                    quit_msg, QMessageBox.Yes, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def close_opencv(self):
        self.opencv.close_opencv()

    def start_opencv(self):
        self.save_as_button.setEnabled(True)
        self.save_as_button.setToolTip("Save composed image")
        self.save_as_action.setEnabled(True)
        self.save_as_action_zenly.setEnabled(True)
        edit_handle = ctypes.windll.user32.FindWindowW(None, "Edit")
        ctypes.windll.user32.ShowWindow(edit_handle, 1)
        self.opencv.main_loop(path_1=img_path_1, path_2=img_path_2, path_3=img_path_3, path_4=img_path_4)

    def save_file_dialog(self):
        if os.path.basename(img_path_1) != "screenshot_1.png" and os.path.basename(img_path_1) != "bg_image.png":
            cur_path = os.path.dirname(img_path_1)
        else:
            cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            # cur_path = "d:/"
        save_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", cur_path+"/Image.jpg",
                                                                  "Image (*.jpg);;Image (*.png)")
        if save_file_name:
            self.opencv.save_image(save_file_name)

    def save_file_dialog_zenly(self):
        if os.path.basename(img_path_1) != "screenshot_1.png" and os.path.basename(img_path_1) != "bg_image.png":
            cur_path = os.path.dirname(img_path_1)
        else:
            cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            # cur_path = "d:/"
        save_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Three Images for Zenly Project", cur_path+"/Image.jpg",
                                                                  "Image (*.jpg);;Image (*.png)")
        if save_file_name:
            self.opencv.save_image_zenly(save_file_name)

    def hide_me_for_screenshot(self, i, s):
        self.hide()
        # QtCore.QTimer.singleShot(300, self.show)
        QtCore.QTimer.singleShot(200, lambda: self.make_screenshot(i, s))

    def make_screenshot(self, i, scrn):
        print(scrn)
        global img_path_1, img_path_2, img_path_3, img_path_4
        # screen = QtWidgets.QApplication.primaryScreen()
        screen = QtWidgets.QApplication.screens()[scrn]
        screenshot = screen.grabWindow(0)
        filename = "img/screenshot_" + str(int(i)) + ".png"
        screenshot.save(filename, 'png')
        if self.opencv.screenshot_region(i):
            self.show()
            icon = QtGui.QPixmap(filename)
            if i == 1:
                self.photoViewer_01.setPixmap(icon.scaled(self.photoViewer_01.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                                                          QtCore.Qt.SmoothTransformation))
                img_path_1 = filename
                self.photoViewer_01.file_path = filename
            if i == 2:
                self.photoViewer_02.setPixmap(icon.scaled(self.photoViewer_02.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                                                          QtCore.Qt.SmoothTransformation))
                img_path_2 = filename
                self.photoViewer_02.file_path = filename
            if i == 3:
                self.photoViewer_03.setPixmap(icon.scaled(self.photoViewer_03.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                                                          QtCore.Qt.SmoothTransformation))
                img_path_3 = filename
                self.photoViewer_03.file_path = filename
            if i == 4:
                self.photoViewer_04.setPixmap(icon.scaled(self.photoViewer_04.size(), QtCore.Qt.KeepAspectRatioByExpanding,
                                                          QtCore.Qt.SmoothTransformation))
                img_path_4 = filename
                self.photoViewer_04.file_path = filename
        self.show()


# ##############################
#  CLASS Opencv
# ##############################
class Opencv:
    def __init__(self):
        # Attributes and variables
        global width1, width2, height1, height2, tr_x, tr_y, zoom, save_resolution
        self.img_1 = None
        self.img_2 = None
        self.img_3 = None
        self.img_4 = None
        self.base_resolution = None
        self.base_save_resolution = None
        self.move = False
        self.resize = False
        self.start_x = 0
        self.start_y = 0
        self.pos = None
        self.highlight_pos = None
        self.highlight_color = (220, 220, 0)
        self.save_width1 = None
        self.save_width2 = None
        self.save_height1 = None
        self.save_height2 = None
        self.close_cv = False
        # Screenshot Attributes
        self.screen_x_start = 0
        self.screen_x_end = 0
        self.screen_y_start = 0
        self.screen_y_end = 0
        self.screen_region_done = False
        self.draw = False
        self.show_rectangle = False
        self.screen_move = False
        self.move_start_x = None
        self.move_start_y = None
        self.move_end_x = None
        self.move_end_y = None
        self.loop_type = None

    def screenshot_region(self, i):
        # Window
        cv2.namedWindow("Screenshot Cropping", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Screenshot Cropping", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Mouse
        cv2.setMouseCallback("Screenshot Cropping", self.mouse_screenshot)

        # Images
        screen = cv2.imread("img/screenshot_" + str(int(i)) + ".png")
        zeros = np.zeros(screen.shape, screen.dtype)
        alpha = 0.5
        beta = (1.0 - alpha)
        screen_dark = cv2.addWeighted(screen, alpha, zeros, beta, 0.0)
        while True:
            screen_final = screen_dark.copy()
            if self.show_rectangle:
                y1 = min(self.screen_y_start, self.screen_y_end)
                y2 = max(self.screen_y_start, self.screen_y_end)
                x1 = min(self.screen_x_start, self.screen_x_end)
                x2 = max(self.screen_x_start, self.screen_x_end)
                screen_final[y1:y2, x1:x2, :] = screen[y1:y2, x1:x2, :]
            cv2.putText(screen_final, "Select area of screen to capture", (35, 35), cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 0), 2)
            cv2.putText(screen_final, "SHIFT when selecting - Move selection", (35, 65), cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 0), 2)
            cv2.imshow("Screenshot Cropping", screen_final)

            # Exit Screenshot Crop Loop
            key = cv2.waitKey(1)
            if key == 27:
                break
            if cv2.getWindowProperty("Screenshot Cropping", cv2.WND_PROP_VISIBLE) < 1:
                print("cv2.WND_PROP_VISIBLE")
                break
            if self.screen_region_done:
                break
        # Crop done (True) or exit without crop (False)
        if self.screen_region_done:
            ret = True
        else:
            ret = False
        # Close Crop Window
        cv2.destroyWindow("Screenshot Cropping")
        # Save Image
        if self.screen_region_done:
            y1 = min(self.screen_y_start, self.screen_y_end)
            y2 = max(self.screen_y_start, self.screen_y_end)
            x1 = min(self.screen_x_start, self.screen_x_end)
            x2 = max(self.screen_x_start, self.screen_x_end)
            cv2.imwrite("img/screenshot_" + str(int(i)) + ".png", screen[y1:y2, x1:x2])
        # Screenshot Attributes
        self.screen_x_start = 0
        self.screen_x_end = 0
        self.screen_y_start = 0
        self.screen_y_end = 0
        self.screen_region_done = False
        self.draw = False
        return ret


    def mouse_screenshot(self, event, x, y, flags, params):
        # If Left Mouse Button Down
        if event == cv2.EVENT_LBUTTONDOWN:
            self.screen_x_start = x
            self.screen_y_start = y
            self.draw = True
        # If Left Mouse Button Up
        elif event == cv2.EVENT_LBUTTONUP:
            self.screen_x_end = x
            self.screen_y_end = y
            self.screen_region_done = True
            self.draw = False
        # If SHIFT + Mouse Move
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_SHIFTKEY):
            if not self.screen_move:
                self.move_start_x = self.screen_x_start - x
                self.move_start_y = self.screen_y_start - y
                self.move_end_x = self.screen_x_end - x
                self.move_end_y = self.screen_y_end - y
            self.screen_move = True
            self.screen_x_start = self.move_start_x + x
            self.screen_y_start = self.move_start_y + y
            self.screen_x_end = self.move_end_x + x
            self.screen_y_end = self.move_end_y + y
        # If Mouse Move
        elif event == cv2.EVENT_MOUSEMOVE:
            self.screen_move = False
            if self.draw:
                self.screen_x_end = x
                self.screen_y_end = y
                if not self.show_rectangle:
                    self.show_rectangle = True

    # Method defines base resolution for each image using width1, width2, height1, height2 global variables
    # 0:img1, 1:img2, 2:img3, 3:img4, 4:img1+img2, 5:img3+img4, 6:img1+img3, 7:img2+img4, 8:img1+img2+img2+img4
    def set_base_resolution(self):
        self.base_resolution = [(width1, height1),
                                (width2, height1),
                                (width1, height2),
                                (width2, height2)]
                                # (width1+width2, height1),
                                # (width1+width2, height2),
                                # (width1, height1+height2),
                                # (width2, height1+height2),
                                # (width1+width2, height1+height2)]

    # Method defines base save resolution for each image using width1, width2, height1, height2 global variables
    def set_base_save_resolution(self):
        self.base_save_resolution = [(self.save_width1, self.save_height1),
                                     (self.save_width2, self.save_height1),
                                     (self.save_width1, self.save_height2),
                                     (self.save_width2, self.save_height2)]

    # Main OpenCV loop start, creating window and showing edited image
    def main_loop(self, path_1, path_2, path_3, path_4):
        paths_id = []
        self.close_cv = False
        self.set_base_resolution()
        cv2.namedWindow('Edit', cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow("Edit", 50, 50)
        cv2.setMouseCallback('Edit', self.mouse_event)
        paths = [path_1, path_2, path_3, path_4]
        # If 3 empty spaces (One image)
        if paths.count(default_image_path) == 3:
            self.loop_type = 1
            for path in paths:
                if path != default_image_path:
                    self.img_1 = cv2.imread(path)

        # If 2 empty spaces (Two images)
        elif paths.count(default_image_path) == 2:
            self.loop_type = 2
            for path in paths:
                if path != default_image_path:
                    paths_id.append(path)
            self.img_1 = cv2.imread(paths_id[0])
            self.img_2 = cv2.imread(paths_id[1])

        # If no empty spaces (Four images)
        elif paths.count(default_image_path) == 0 or 1:
            self.loop_type = 6
            self.img_1 = cv2.imread(path_1)
            self.img_2 = cv2.imread(path_2)
            self.img_3 = cv2.imread(path_3)
            self.img_4 = cv2.imread(path_4)

        # One Image Loop
        if self.loop_type == 1:
            while not self.close_cv:
                # Create image
                img_1_edit = self.create_image(self.img_1, 0)
                # Stack Image and Highlights
                border_h1 = np.zeros((height1, 2, 3), dtype='uint8')
                border_w1 = np.zeros((2, width1 + 2, 3), dtype='uint8')
                # Vertical highlight
                if self.highlight_pos == 4:
                    border_h1[:, :] = self.highlight_color
                # Horizontal highlight
                if self.highlight_pos == 6:
                    border_w1[:, :] = self.highlight_color
                stack = np.hstack((img_1_edit, border_h1))
                stack = np.vstack((stack, border_w1))
                # Show final image
                try:
                    cv2.imshow("Edit", stack)
                except:
                    print('error!!: ', sys.exc_info()[0])
                # Quit if "q" pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.close_cv = True
                # Quit if "X" pressed
                if cv2.getWindowProperty("Edit", cv2.WND_PROP_VISIBLE) < 1:
                    self.close_cv = True

        # Two Images Loop
        if self.loop_type == 2:
            while not self.close_cv:
                # Create all images
                img_1_edit = self.create_image(self.img_1, 0)
                img_2_edit = self.create_image(self.img_2, 1)

                # Stack Images and Highlight for resize

                # ----- img1 + img2
                border_h1 = np.zeros((height1, 1, 3), dtype='uint8')
                # Vertical highlight
                if self.highlight_pos == 4:
                    border_h1[:, :] = self.highlight_color
                stack1 = np.hstack((img_1_edit, border_h1, img_2_edit))

                border_w = np.zeros((2, width1 + width2 + 1, 3), dtype='uint8')
                # Horizontal highlight
                if self.highlight_pos == 6:
                    border_w[:, :] = self.highlight_color

                # ----- (img1 + img2) + (img3 + img4)
                stack = np.vstack((stack1, border_w))
                # Right Highlight
                if self.highlight_pos == 5:
                    stack[:, -2:] = self.highlight_color

                # Show final image
                try:
                    cv2.imshow("Edit", stack)
                except:
                    print('error!!: ', sys.exc_info()[0])

                # Quit if "q" pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.close_cv = True
                if cv2.getWindowProperty("Edit", cv2.WND_PROP_VISIBLE) < 1:
                    self.close_cv = True
        # Four images
        if self.loop_type == 6:
            while not self.close_cv:
                # Create all images
                img_1_edit = self.create_image(self.img_1, 0)
                img_2_edit = self.create_image(self.img_2, 1)
                img_3_edit = self.create_image(self.img_3, 2)
                img_4_edit = self.create_image(self.img_4, 3)

                # Stack Images and Highlight for resize

                # ----- img1 + img2
                border_h1 = np.zeros((height1, 1, 3), dtype='uint8')
                # Vertical highlight
                if self.highlight_pos == 4:
                    border_h1[:, :] = self.highlight_color
                stack1 = np.hstack((img_1_edit, border_h1, img_2_edit))

                # ----- img3 + img4
                border_h2 = np.zeros((height2, 1, 3), dtype='uint8')
                # Vertical highlight
                if self.highlight_pos == 4:
                    border_h2[:, :] = self.highlight_color
                stack2 = np.hstack((img_3_edit, border_h2, img_4_edit))
                # Bottom highlight
                if self.highlight_pos == 7:
                    stack2[-2:] = self.highlight_color
                border_w = np.zeros((1, width1 + width2 + 1, 3), dtype='uint8')
                # Horizontal highlight
                if self.highlight_pos == 6:
                    border_w[:, :] = self.highlight_color

                # ----- (img1 + img2) + (img3 + img4)
                stack = np.vstack((stack1, border_w, stack2))
                # Right Highlight
                if self.highlight_pos == 5:
                    stack[:, -2:] = self.highlight_color

                # Copyrights
                # cv2.putText(stack, "©Ocellus", (width1 + width2 - 70, height1 + height2 - 15), cv2.FONT_HERSHEY_PLAIN,
                # 0.4, (255, 255, 255), 1, cv2.LINE_AA)

                # Show final image
                try:
                    cv2.imshow("Edit", stack)
                except:
                    print('error!!: ', sys.exc_info()[0])

                # Quit if "q" pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.close_cv = True
                if cv2.getWindowProperty("Edit", cv2.WND_PROP_VISIBLE) < 1:
                    self.close_cv = True

        cv2.destroyAllWindows()

    # Editing (move, scale) image
    def create_image(self, img, i):
        # Local Variables
        border_top, border_bottom, border_left, border_right = 0, 0, 0, 0
        y, x = img.shape[:2]

        # Region coordinates to crop in world
        crop_x_start = int(x / 2 - self.base_resolution[i][0] / zoom[i] / 2 - tr_x[i] / zoom[i])
        crop_x_end = int(crop_x_start + self.base_resolution[i][0] / zoom[i])
        crop_y_start = int(y / 2 - self.base_resolution[i][1] / zoom[i] / 2 - tr_y[i] / zoom[i])
        crop_y_end = int(crop_y_start + self.base_resolution[i][1] / zoom[i])

        # Region to crop on image (without negative values)
        crop_y_region_start = max(0, crop_y_start)
        crop_x_region_start = max(0, crop_x_start)
        img_edit = img[crop_y_region_start:crop_y_end, crop_x_region_start:crop_x_end, :]

        # Adding borders on cropped image if needed
        if crop_x_start < 0:
            border_left = crop_x_start * (-1)
        if crop_y_start < 0:
            border_top = crop_y_start * (-1)
        if crop_x_end > x:
            border_right = crop_x_end - x
        if crop_y_end > y:
            border_bottom = crop_y_end - y
        img_edit = cv2.copyMakeBorder(img_edit, border_top, border_bottom, border_left, border_right,
                                      cv2.BORDER_REPLICATE)
        img_edit = cv2.resize(img_edit, self.base_resolution[i], interpolation=cv2.INTER_AREA)
        return img_edit

    # Editing (move, scale) image for save (higher resolution)
    def create_save_image(self, img, i):
        # Local Variables
        border_top, border_bottom, border_left, border_right = 0, 0, 0, 0
        y, x = img.shape[:2]

        # Region coordinates to crop in world
        crop_x_start = int(x / 2 - self.base_resolution[i][0] / zoom[i] / 2 - tr_x[i] / zoom[i])
        crop_x_end = int(crop_x_start + self.base_resolution[i][0] / zoom[i])
        crop_y_start = int(y / 2 - self.base_resolution[i][1] / zoom[i] / 2 - tr_y[i] / zoom[i])
        crop_y_end = int(crop_y_start + self.base_resolution[i][1] / zoom[i])

        # Region to crop on image (without negative values)
        crop_y_region_start = max(0, crop_y_start)
        crop_x_region_start = max(0, crop_x_start)
        img_edit = img[crop_y_region_start:crop_y_end, crop_x_region_start:crop_x_end, :]

        # Adding borders on cropped image if needed
        if crop_x_start < 0:
            border_left = crop_x_start * (-1)
        if crop_y_start < 0:
            border_top = crop_y_start * (-1)
        if crop_x_end > x:
            border_right = crop_x_end - x
        if crop_y_end > y:
            border_bottom = crop_y_end - y
        img_edit = cv2.copyMakeBorder(img_edit, border_top, border_bottom, border_left, border_right,
                                      cv2.BORDER_REPLICATE)
        img_edit = cv2.resize(img_edit, self.base_save_resolution[i], interpolation=cv2.INTER_AREA)
        return img_edit

    # Save Image
    def save_image(self, path):
        if self.loop_type == 1:
            current_resolution = width1 / zoom[0]
            # Calculating resolution for save image
            if current_resolution < save_resolution:
                self.save_width1 = int(width1 / min(zoom))
                self.save_width2 = int(width2 / min(zoom))
                self.save_height1 = int(height1 / min(zoom))
                self.save_height2 = int(height2 / min(zoom))
            else:
                coefficient = 1600 / width1
                self.save_width1 = int(width1 * coefficient)
                self.save_width2 = int(width2 * coefficient)
                self.save_height1 = int(height1 * coefficient)
                self.save_height2 = int(height2 * coefficient)

            self.set_base_save_resolution()

            # Creating save images
            img_1_save = self.create_save_image(self.img_1, 0)
            stack = img_1_save
            # Stacking save images
            # border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
            # stack = np.hstack((img_1_save, border_h1, img_2_save))
            cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
                          (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)
            cv2.imwrite(path, stack)

        if self.loop_type == 2:
            current_resolution = (width1 + width2) / min(zoom[0], zoom[1])
            # Calculating resolution for save image
            if current_resolution < save_resolution:
                self.save_width1 = int(width1 / min(zoom))
                self.save_width2 = int(width2 / min(zoom))
                self.save_height1 = int(height1 / min(zoom))
                self.save_height2 = int(height2 / min(zoom))
            else:
                coefficient = 1600 / (width1 + width2)
                self.save_width1 = int(width1 * coefficient)
                self.save_width2 = int(width2 * coefficient)
                self.save_height1 = int(height1 * coefficient)
                self.save_height2 = int(height2 * coefficient)

            self.set_base_save_resolution()

            # Creating save images
            img_1_save = self.create_save_image(self.img_1, 0)
            img_2_save = self.create_save_image(self.img_2, 1)

            # Stacking save images
            border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
            stack = np.hstack((img_1_save, border_h1, img_2_save))
            cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
                          (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)

            cv2.imwrite(path, stack)

        if self.loop_type == 6:
            current_resolution = (width1 + width2) / min(zoom)
            # Calculating resolution for save image
            if current_resolution < save_resolution:
                self.save_width1 = int(width1 / min(zoom))
                self.save_width2 = int(width2 / min(zoom))
                self.save_height1 = int(height1 / min(zoom))
                self.save_height2 = int(height2 / min(zoom))
            else:
                coefficient = 1600 / (width1 + width2)
                self.save_width1 = int(width1 * coefficient)
                self.save_width2 = int(width2 * coefficient)
                self.save_height1 = int(height1 * coefficient)
                self.save_height2 = int(height2 * coefficient)

            self.set_base_save_resolution()

            # Creating save images
            img_1_save = self.create_save_image(self.img_1, 0)
            img_2_save = self.create_save_image(self.img_2, 1)
            img_3_save = self.create_save_image(self.img_3, 2)
            img_4_save = self.create_save_image(self.img_4, 3)

            # Stacking save images
            border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
            stack1 = np.hstack((img_1_save, border_h1, img_2_save))
            border_h2 = np.zeros((self.save_height2, 1, 3), dtype='uint8')
            stack2 = np.hstack((img_3_save, border_h2, img_4_save))
            border_w = np.zeros((1, self.save_width1 + self.save_width2 + 1, 3), dtype='uint8')
            stack = np.vstack((stack1, border_w, stack2))
            cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
                          (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)

            cv2.imwrite(path, stack)

    # Save Image for Zenly (Saving 3 images)
    def save_image_zenly(self, path):
        if self.loop_type == 6:
            current_resolution = (width1 + width2) / min(zoom)
            # Calculating resolution for save image
            if current_resolution < save_resolution:
                self.save_width1 = int(width1 / min(zoom))
                self.save_width2 = int(width2 / min(zoom))
                self.save_height1 = int(height1 / min(zoom))
                self.save_height2 = int(height2 / min(zoom))
            else:
                coefficient = 1600 / (width1 + width2)
                self.save_width1 = int(width1 * coefficient)
                self.save_width2 = int(width2 * coefficient)
                self.save_height1 = int(height1 * coefficient)
                self.save_height2 = int(height2 * coefficient)

            self.set_base_save_resolution()

            # Creating save images
            img_1_save = self.create_save_image(self.img_1, 0)
            img_2_save = self.create_save_image(self.img_2, 1)
            img_3_save = self.create_save_image(self.img_3, 2)
            img_4_save = self.create_save_image(self.img_4, 3)

            # Stacking save images
            border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
            stack1 = np.hstack((img_1_save, border_h1, img_2_save))

            border_h2 = np.zeros((self.save_height2, 1, 3), dtype='uint8')
            stack2 = np.hstack((img_3_save, border_h2, img_4_save))

            border_w = np.zeros((1, self.save_width1 + self.save_width2 + 1, 3), dtype='uint8')
            stack = np.vstack((stack1, border_w, stack2))
            cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
                          (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)

            cv2.imwrite(path[:-4] + "_SC_Engine_00" + path[-4:], stack1)
            cv2.imwrite(path[:-4] + "_SC_DDC_00" + path[-4:], stack2)
            cv2.imwrite(path, stack)


    # When mouse event runs this method
    def mouse_event(self, event, x, y, flags, params):
        # Global Variables
        global width1, width2, height1, height2
        # If Left Mouse Button Down
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pos = self.mouse_tile_position(x, y)
            if self.pos < 4:
                self.move = True
                self.start_x, self.start_y = x - tr_x[self.pos], y - tr_y[self.pos]
            else:
                self.resize = True
        # If Left Mouse Button Up
        elif event == cv2.EVENT_LBUTTONUP:
            self.resize = False
            self.move = False
        # If Mouse Move
        elif event == cv2.EVENT_MOUSEMOVE:
            self.highlight_pos = self.mouse_tile_position(x, y)
            if self.move:
                tr_x[self.pos], tr_y[self.pos] = x - self.start_x, y - self.start_y
            if self.resize:
                # Vertical Middle
                if self.pos == 4:
                    if ((width2 - (x - width1)) > 100) and (x > 100):
                        width2 = width2 - (x - width1)
                        width1 = x
                # Vertical Right
                elif self.pos == 5:
                    delta = int((x - (width2 + width1 + 1)) / 2)
                    if ((width1 + delta) > 100) and ((width2 + delta) > 100):
                        width1 = width1 + delta
                        width2 = width2 + delta
                    elif ((width1 + delta) > 100) and ((width2 + delta) < 100):
                        width1 = width1 + delta * 2
                    elif ((width1 + delta) < 100) and ((width2 + delta) > 100):
                        width2 = width2 + delta * 2
                # Horizontal Middle
                elif self.pos == 6:
                    if ((height2 - (y - height1)) > 75) and (y > 75):
                        height2 = height2 - (y - height1)
                        height1 = y
                # Horizontal Bottom
                elif self.pos == 7:
                    delta = int((y - (height2 + height1 + 1)) / 2)
                    if ((height1 + delta) > 75) and ((height2 + delta) > 75):
                        height1 = height1 + delta
                        height2 = height2 + delta
                    if ((height1 + delta) > 75) and ((height2 + delta) < 75):
                        height1 = height1 + delta
                    if ((height1 + delta) < 75) and ((height2 + delta) > 75):
                        height2 = height2 + delta
                # self.set_base_resolution()
                # width1 = max(width1, 100)
                # width2 = max(width2, 100)
                # height1 = max(height1, 50)
                # height2 = max(height2, 50)
                self.set_base_resolution()
        # If Mouse Wheel Scroll
        elif event == cv2.EVENT_MOUSEWHEEL:
            self.pos = self.mouse_tile_position(x, y)
            if flags > 0:
                zoom[self.pos] *= 1.1
            else:
                zoom[self.pos] /= 1.1

    # Function returns current tile number using mouse position
    @staticmethod
    def mouse_tile_position(x, y):
        if x < width1 - 4:
            if y < height1 - 4:
                return 0
            elif (y >= height1 - 4) and (y <= height1 + 5):
                return 6
            elif (y > height1 + 4) and (y < height1 + 1 + height2 - 9):
                return 2
            else:
                return 7
        elif (x >= width1 - 4) and (x <= width1 + 5):
            return 4
        elif (x > width1 + 5) and (x < width1 + 1 + width2 - 9):
            if y < height1 - 4:
                return 1
            elif (y >= height1 - 4) and (y <= height1 + 5):
                return 6
            elif (y > height1 + 5) and (y < height1 + 1 + height2 - 9):
                return 3
            else:
                return 7
        else:
            return 5

    # Close OpenCV
    def close_opencv(self):
        self.close_cv = True


current_year = date.today().year
if current_year < 2023:
    # Global Variables
    version = "1.0.3"
    width1, width2 = 450, 450
    height1, height2 = 350, 350
    tr_x = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    tr_y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    zoom = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    save_resolution = 1600
    default_image_path = "./img/bg_image.png"

    # # Temporary assignment for testing
    # img_path_1 = "C:/Users/Alexander/Desktop/Ch_01.jpg"
    # img_path_2 = "C:/Users/Alexander/Desktop/Ch_02.jpg"
    # img_path_3 = "C:/Users/Alexander/Desktop/Ch_03.jpg"
    # img_path_4 = "C:/Users/Alexander/Desktop/Ch_04.jpg"

    # Default Image Assignment
    img_path_1 = default_image_path
    img_path_2 = default_image_path
    img_path_3 = default_image_path
    img_path_4 = default_image_path

    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
