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
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n or Take a Screenshot \n\n")
        # self.setScaledContents(True)
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
            }
        ''')
        self.setAcceptDrops(True)
        self.file_path = ""
        self.setScaledContents(False)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        # self.setFixedSize(100, 100)

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
        icon = QtGui.QPixmap(file_path)
        self.setPixmap(icon.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.assignImagePath(self.objectName(), file_path)

    # Set "img_paths" Global Variable
    def assignImagePath(self, obj_name, path):
        global img_paths
        col = obj_name[15:17]
        row = obj_name[12:14]
        img_paths[int(row)][int(col)] = path


# ##############################
#  CLASS MainWindow
# ##############################
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pyqt_num_of_cols = 2
        self.pyqt_num_of_rows = 2


        # Main Window
        # self.setFixedSize(430, 520)
        # self.setGeometry(1200, 200, 430, 520)
        self.setWindowTitle("Image Grid v." + version + "   (lecense: Ocellus Studio)")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

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

        # OpenCV
        self.opencv = Opencv()

        # Button connect
        self.transfer_button.clicked.connect(self.start_opencv)
        self.save_as_button.clicked.connect(self.save_file_dialog)
        self.exit_button.clicked.connect(self.close_opencv)

        # Layout
        self.main_layout = QtWidgets.QGridLayout()

        # Elements Creation
        self.make_menu_bar()

        # New Image Grid
        self.main_grid_layout = QtWidgets.QGridLayout()

        self.top_buttons_layout = QtWidgets.QHBoxLayout()
        self.left_buttons_layout = QtWidgets.QVBoxLayout()
        self.images_layout = QtWidgets.QVBoxLayout()
        self.right_button_layout = QtWidgets.QHBoxLayout()
        self.bottom_button_layout = QtWidgets.QHBoxLayout()


        # Main Layout
        self.main_grid_layout.addLayout(self.top_buttons_layout, 0, 1)
        self.main_grid_layout.addLayout(self.left_buttons_layout, 1, 0)
        self.main_grid_layout.addLayout(self.images_layout, 1, 1)
        self.main_grid_layout.addLayout(self.right_button_layout, 1, 2)
        self.main_grid_layout.addLayout(self.bottom_button_layout, 2, 1)

        self.construct_grid()

        # Main Layout
        self.main_layout.addWidget(self.menu_bar, 0, 0, 1, 2)
        self.main_layout.addWidget(self.line_menu, 1, 0, 1, 2)
        self.main_layout.addLayout(self.main_grid_layout, 4, 0, 1, 2)
        self.main_layout.addWidget(self.line, 6, 0, 1, 2)
        self.main_layout.addWidget(self.transfer_button, 7, 0, 1, 1)
        self.main_layout.addWidget(self.save_as_button, 7, 1, 1, 1)

        self.setLayout(self.main_layout)

    # Creation of Images Grid
    def construct_grid(self):

        self.photoViewer = [[0 for i in range(self.pyqt_num_of_cols)] for j in range(self.pyqt_num_of_rows)]

        # Clear Images Grid Layouts
        self.clear_layout(self.top_buttons_layout)
        self.clear_layout(self.left_buttons_layout)
        self.clear_layout(self.images_layout)
        self.clear_layout(self.right_button_layout)
        self.clear_layout(self.bottom_button_layout)

        # Top Buttons Layout
        for c in range(self.pyqt_num_of_cols):
            elem_layout = QtWidgets.QHBoxLayout()
            button1 = QtWidgets.QPushButton()
            button1.setToolTip('Merge column')
            if combined_cols[c] == 1:
                button1.setIcon(QtGui.QIcon("./img/SVG/demerge-column-color.svg"))
            else:
                button1.setIcon(QtGui.QIcon("./img/SVG/merge-column-color.svg"))
            button1.clicked.connect(lambda state, x=c: self.combine_column(x))
            button2 = QtWidgets.QPushButton()
            button2.setToolTip('Delete column')
            button2.setIcon(QtGui.QIcon("./img/SVG/del-column-color.svg"))
            button2.setFixedWidth(30)
            button2.clicked.connect(lambda state, x=c: self.remove_column(x))
            elem_layout.addWidget(button1)
            elem_layout.addWidget(button2)
            elem_layout.setSpacing(0)
            self.top_buttons_layout.addLayout(elem_layout)

        # Left Buttons Layout
        for r in range(self.pyqt_num_of_rows):
            elem_layout = QtWidgets.QVBoxLayout()
            button1 = QtWidgets.QPushButton()
            button1.setToolTip('Merge row')
            if combined_rows[r] == 1:
                button1.setIcon(QtGui.QIcon("./img/SVG/demerge-row-color.svg"))
            else:
                button1.setIcon(QtGui.QIcon("./img/SVG/merge-row-color.svg"))
            button1.clicked.connect(lambda state, x=r: self.combine_row(x))
            button1.setFixedWidth(25)
            button1.setSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Expanding)
            button2 = QtWidgets.QPushButton()
            button2.setToolTip('Delete row')
            button2.setIcon(QtGui.QIcon("./img/SVG/del-row-color.svg"))
            button2.clicked.connect(lambda state, x=r: self.remove_row(x))
            button2.setFixedWidth(25)
            button2.setFixedHeight(25)
            button2.setSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Expanding)
            elem_layout.addWidget(button1)
            elem_layout.addWidget(button2)
            elem_layout.setSpacing(0)
            self.left_buttons_layout.addLayout(elem_layout)

        # Images Layout
        # Labels for Images Creation
        for r in range(self.pyqt_num_of_rows):
            for c in range(self.pyqt_num_of_cols):
                self.photoViewer[r][c] = self.construct_label(r, c)

        # If we don't have combined columns
        if not any(combined_cols):
            print("ROWS PyQt")
            images_vertical_layout = QtWidgets.QVBoxLayout()
            self.images_layout.addLayout(images_vertical_layout)
            for r in range(self.pyqt_num_of_rows):
                row_layout = QtWidgets.QHBoxLayout()
                self.images_layout.addLayout(row_layout)
                # If current row combined
                if combined_rows[r]:
                    elem_layout = QtWidgets.QVBoxLayout()
                    row_layout.addLayout(elem_layout)
                    elem_layout.addWidget(self.photoViewer[r][0])
                    elem_layout.addLayout(self.construct_screenshot_layout(r, 0))
                    elem_layout.setSpacing(2)
                # If current row not combined
                else:
                    for c in range(self.pyqt_num_of_cols):
                        elem_layout = QtWidgets.QVBoxLayout()
                        row_layout.addLayout(elem_layout)
                        elem_layout.addWidget(self.photoViewer[r][c])
                        elem_layout.addLayout(self.construct_screenshot_layout(r, c))
                        elem_layout.setSpacing(2)
        # If we have combined columns
        else:
            print("COLUMNS PyQt")
            images_horizontal_layout = QtWidgets.QHBoxLayout()
            self.images_layout.addLayout(images_horizontal_layout)
            for c in range(self.pyqt_num_of_cols):
                column_layout = QtWidgets.QVBoxLayout()
                images_horizontal_layout.addLayout(column_layout)
                # If current column combined
                if combined_cols[c]:
                    elem_layout = QtWidgets.QVBoxLayout()
                    column_layout.addLayout(elem_layout)
                    # self.photoViewer[0][c] = self.construct_label(0, c)
                    # button = QtWidgets.QPushButton("Screenshot " + str(r) + "-" + str(c))
                    elem_layout.addWidget(self.photoViewer[0][c])
                    elem_layout.addLayout(self.construct_screenshot_layout(0, c))
                    elem_layout.setSpacing(2)
                # If current row not combined
                else:
                    for r in range(self.pyqt_num_of_rows):
                        elem_layout = QtWidgets.QVBoxLayout()
                        column_layout.addLayout(elem_layout)
                        elem_layout.addWidget(self.photoViewer[r][c])
                        elem_layout.addLayout(self.construct_screenshot_layout(r, c))
                        elem_layout.setSpacing(2)

        # Right Button Layout
        button = QtWidgets.QPushButton()
        button.setToolTip('Add new column')
        button.setIcon(QtGui.QIcon("./img/SVG/add-column-color.svg"))
        button.setIconSize(QtCore.QSize(20, 20))
        button.setFixedWidth(40)
        button.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding)
        button.clicked.connect(self.add_column)
        self.right_button_layout.addWidget(button)

        # Bottom Button Layout
        button = QtWidgets.QPushButton()
        button.setIcon(QtGui.QIcon("./img/SVG/add-row-color.svg"))
        button.setToolTip('Add new row')
        button.setIconSize(QtCore.QSize(20, 20))
        button.clicked.connect(self.add_row)
        button.setFixedHeight(40)
        self.bottom_button_layout.addWidget(button)
        # Using setFixedSize: (width, height)
        self.setFixedSize(150 * self.pyqt_num_of_cols + 180, 130 * self.pyqt_num_of_rows + 180 + 100)
        QtCore.QTimer.singleShot(1, lambda: self.show_grid_images())

    def construct_screenshot_layout(self, r, c):
        # Screenshot Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        # Screenshor Buttons
        screen_btn1 = QtWidgets.QPushButton("  Screenshot")
        screen_btn1.setToolTip("Screenshot of the first monitor")
        screen_btn1.setIcon(QtGui.QIcon('img\monitor_1.png'))
        screen_btn2 = QtWidgets.QPushButton()
        screen_btn2.setMaximumWidth(28)
        screen_btn2.setToolTip("Screenshot of second monitor")
        screen_btn2.setIcon(QtGui.QIcon('img\monitor_2.png'))
        screen_btn3 = QtWidgets.QPushButton()
        screen_btn3.setMaximumWidth(28)
        screen_btn3.setToolTip("Screenshot of third monitor")
        screen_btn3.setIcon(QtGui.QIcon('img\monitor_3.png'))
        # Adding Buttons to Layout
        layout.addWidget(screen_btn1)
        if len(QApplication.screens()) > 1:
            layout.addWidget(self.screen_btn2)
        if len(QApplication.screens()) > 2:
            layout.addWidget(self.screen_btn3)
        # Clicked Connect
        screen_btn1.clicked.connect(lambda state, x=r, y=c: self.hide_me_for_screenshot(0, x, y))
        screen_btn2.clicked.connect(lambda state, x=r, y=c: self.hide_me_for_screenshot(1, x, y))
        screen_btn3.clicked.connect(lambda state, x=r, y=c: self.hide_me_for_screenshot(2, x, y))

        return layout

    # Place images in labels
    def show_grid_images(self):
        for r in range(self.pyqt_num_of_rows):
            for c in range(self.pyqt_num_of_cols):
                self.photoViewer[r][c].set_image(img_paths[r][c])

    # Dimensions of multidimensional list
    def dim(self, a):
        if not type(a) == list:
            return []
        return [len(a)] + self.dim(a[0])

    def construct_label(self, r, c):
        label = ImageLabel()
        label.setObjectName(f"photoViewer_{r:02}_{c:02}")
        return label

    def add_column(self):
        if self.pyqt_num_of_cols < 15:
            self.pyqt_num_of_cols += 1
            self.construct_grid()

    def remove_column(self, number):
        global combined_cols
        global img_paths,  default_image_path
        if self.pyqt_num_of_cols > 1:
            self.pyqt_num_of_cols -= 1
            combined_cols.pop(number)
            combined_cols.append(False)
            for i in img_paths:
                i.pop(number)
                i.append(default_image_path)
            self.construct_grid()

    def add_row(self):
        if self.pyqt_num_of_rows < 7:
            self.pyqt_num_of_rows += 1
            self.construct_grid()

    def remove_row(self, number):
        global combined_rows
        global img_paths, default_image_path
        if self.pyqt_num_of_rows > 1:
            self.pyqt_num_of_rows -= 1
            combined_rows.pop(number)
            combined_rows.append(False)
            self.construct_grid()
            img_paths.pop(number)
            img_paths.append([default_image_path] * 15)

    def combine_column(self, number):
        global combined_rows, combined_cols, any_col_combined, any_row_combined
        combined_rows = [False] * 7
        any_row_combined = False
        combined_cols[number] = not combined_cols[number]
        if any(combined_cols):
            any_col_combined = True

        self.construct_grid()

    def combine_row(self, number):
        global combined_rows, combined_cols, any_col_combined, any_row_combined
        combined_cols = [False] * 15
        any_col_combined = False
        combined_rows[number] = not combined_rows[number]
        if any(combined_rows):
            any_row_combined = True
        self.construct_grid()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

    def make_menu_bar(self):
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

    def show_about(self):
        print("show about")
        about_box = QMessageBox()
        # about_box.setFixedSize(500, 200);
        about_box.setIcon(QMessageBox.Information)
        about_box.setWindowTitle("About")
        about_box.setText("  Image Grid v" + version + "   \n\n           2022         \n by Alexander Kovalev \n kovalev.cg@gmail.com")
        about_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        about_box.exec_()

    def closeEvent(self, event):
        self.close_opencv()
        event.accept()

    def close_opencv(self):
        self.opencv.close_opencv()

    def start_opencv(self):
        self.save_as_button.setEnabled(True)
        self.save_as_button.setToolTip("Save composed image")
        self.save_as_action.setEnabled(True)
        self.save_as_action_zenly.setEnabled(True)
        edit_handle = ctypes.windll.user32.FindWindowW(None, "Edit")
        ctypes.windll.user32.ShowWindow(edit_handle, 1)
        self.opencv.main_loop(self.pyqt_num_of_cols, self.pyqt_num_of_rows)
        # , combined_rows, combined_cols

    def save_file_dialog(self):
        # if os.path.basename(img_path_1) != "screenshot_1.png" and os.path.basename(img_path_1) != "bg_image.png":
        #     cur_path = os.path.dirname(img_path_1)
        # else:
        cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        # cur_path = "d:/"
        save_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", cur_path+"/Image.jpg",
                                                                  "Image (*.jpg);;Image (*.png)")
        if save_file_name:
            self.opencv.save_image(save_file_name)

    def save_file_dialog_zenly(self):
        # if os.path.basename(img_path_1) != "screenshot_1.png" and os.path.basename(img_path_1) != "bg_image.png":
        #     cur_path = os.path.dirname(img_path_1)
        # else:
        cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        # cur_path = "d:/"
        save_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Three Images for Zenly Project", cur_path+"/Image.jpg",
                                                                  "Image (*.jpg);;Image (*.png)")
        if save_file_name:
            self.opencv.save_image_zenly(save_file_name)

    def hide_me_for_screenshot(self, s, r, c):
        self.hide()
        QtCore.QTimer.singleShot(200, lambda: self.make_screenshot(s, r, c))

    def make_screenshot(self, scrn, r, c):
        global img_paths
        print(f"screen: {scrn}")
        screen = QtWidgets.QApplication.screens()[scrn]
        screenshot = screen.grabWindow(0)
        filename = f"img/screenshot_{r:02}_{c:02}.png"
        screenshot.save(filename, 'png')

        if self.opencv.screenshot_region(r, c):
            self.show()
            icon = QtGui.QPixmap(filename)
            self.photoViewer[r][c].setPixmap(icon.scaled(self.photoViewer[r][c].size(), QtCore.Qt.KeepAspectRatioByExpanding,
                                                      QtCore.Qt.SmoothTransformation))
            img_paths[r][c] = filename

        self.show()


# ##############################
#  CLASS Opencv
# ##############################
class Opencv:
    def __init__(self):
        # Attributes and variables
        global start_width, start_height, tr_x, tr_y, zoom
        self.move = False
        self.resize = False
        self.start_x = 0
        self.start_y = 0
        self.mouse_on_type = None
        self.mouse_on_num = None
        self.mouse_on_arr = [None, None]
        self.highlight_color = (220, 220, 0)
        self.images = []
        # self.save_width1 = None
        # self.save_width2 = None
        # self.save_height1 = None
        # self.save_height2 = None
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

    def screenshot_region(self, r, c):
        # Window
        cv2.namedWindow("Screenshot Cropping", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Screenshot Cropping", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Mouse
        cv2.setMouseCallback("Screenshot Cropping", self.mouse_screenshot)

        # Images
        # screen = cv2.imread("img/screenshot_" + str(int(i)) + ".png")
        screen = cv2.imread(f"img/screenshot_{r:02}_{c:02}.png")
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
                # print("cv2.WND_PROP_VISIBLE")
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
            cv2.imwrite(f"img/screenshot_{r:02}_{c:02}.png", screen[y1:y2, x1:x2])
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

    # # Method defines base resolution for each image using width1, width2, height1, height2 global variables
    # # 0:img1, 1:img2, 2:img3, 3:img4, 4:img1+img2, 5:img3+img4, 6:img1+img3, 7:img2+img4, 8:img1+img2+img2+img4
    # def set_base_resolution(self):
    #     self.base_resolution = [(width1, height1),
    #                             (width2, height1),
    #                             (width1, height2),
    #                             (width2, height2)]
    #                             # (width1+width2, height1),
    #                             # (width1+width2, height2),
    #                             # (width1, height1+height2),
    #                             # (width2, height1+height2),
    #                             # (width1+width2, height1+height2)]
    #
    # # Method defines base save resolution for each image using width1, width2, height1, height2 global variables
    # def set_base_save_resolution(self):
    #     self.base_save_resolution = [(self.save_width1, self.save_height1),
    #                                  (self.save_width2, self.save_height1),
    #                                  (self.save_width1, self.save_height2),
    #                                  (self.save_width2, self.save_height2)]

    def set_total_resolution(self):
        global width_total, height_total, num_of_rows, num_of_cols
        width_total = 0
        height_total = 0
        for c in range(num_of_cols):
            width_total += cell_widths[c]
        for r in range(num_of_rows):
            height_total += cell_heights[r]
        width_total += num_of_cols + 1
        height_total += num_of_rows + 1

    #
    # Main OpenCV loop start, creating window and showing edited image
    #
    def main_loop(self, num_of_c, num_of_r):
        global img_paths, cell_widths, cell_heights, width_total, height_total, num_of_cols,  num_of_rows

        print("START of OpenCV - MAIN LOOP")

        self.close_cv = False
        cv2.namedWindow('Edit', cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow("Edit", 50, 50)
        cv2.setMouseCallback('Edit', self.mouse_event)

        # Reset sizes if number of rows or cols changed
        if (num_of_cols != num_of_c) or (num_of_rows != num_of_r):
            num_of_cols = num_of_c
            num_of_rows = num_of_r

            # Set Initial Cell Sizes
            for r in range(num_of_rows):
                cell_heights[r] = int(start_height / num_of_rows)
            for c in range(num_of_cols):
                cell_widths[c] = int(start_width / num_of_cols)

        # width_total and height_total
        self.set_total_resolution()

        # Read Images
        self.images = [[0 for i in range(num_of_cols)] for j in range(num_of_rows)]
        for r in range(num_of_rows):
            for c in range(num_of_cols):
                self.images[r][c] = cv2.imread(img_paths[r][c])
        # print(self.images)

        # Any Amount of Images Loop
        while not self.close_cv:

            # Stack Images
            # If we don't have combined columns
            if not any_col_combined:
                # print("ROWS")
                border_w = np.zeros((1, width_total, 3), dtype='uint8')
                border_w_highlighted = border_w.copy()
                border_w_highlighted[:, :] = self.highlight_color
                stack = border_w.copy()
                for row in range(num_of_rows):
                    # If current row combined
                    if combined_rows[row]:
                        stack_r = self.create_image(self.images[row][0], row, 0, combined="rows")
                    # If current row not combined
                    else:
                        # Usual image border and highlighted border
                        border_h = np.zeros((cell_heights[row], 1, 3), dtype='uint8')
                        border_h_highlighted = border_h.copy()
                        border_h_highlighted[:, :] = self.highlight_color
                        stack_r = border_h.copy()
                        # Loop all cols
                        for col in range(num_of_cols):
                            # Image creation
                            img_edit = self.create_image(self.images[row][col], row, col, combined="none")
                            # Adding usual or highlighted border
                            if self.mouse_on_type == "grid_v" and self.mouse_on_num == col:
                                stack_r = np.hstack((stack_r, img_edit, border_h_highlighted))
                            else:
                                stack_r = np.hstack((stack_r, img_edit, border_h))
                    if self.mouse_on_type == "grid_h" and self.mouse_on_num == row:
                        stack = np.vstack((stack, stack_r, border_w_highlighted))
                    else:
                        stack = np.vstack((stack, stack_r, border_w))

            # If we have combined columns
            else:
                # print("COLUMNS")
                border_h = np.zeros((height_total, 1, 3), dtype='uint8')
                border_h_highlighted = border_h.copy()
                border_h_highlighted[:, :] = self.highlight_color
                stack = border_h.copy()
                for col in range(num_of_cols):
                    # If current column combined

                    if combined_cols[col]:
                        stack_c = self.create_image(self.images[0][col], 0, col, combined="columns")
                    # If current column not combined
                    else:
                        # Usual image border and highlighted border
                        border_w = np.zeros((1, cell_widths[col], 3), dtype='uint8')
                        border_w_highlighted = border_w.copy()
                        border_w_highlighted[:, :] = self.highlight_color
                        stack_c = border_w.copy()
                        # Loop all rows
                        for row in range(num_of_rows):
                            # Image creation
                            img_edit = self.create_image(self.images[row][col], row, col, combined="none")
                            # Adding usual or highlighted border
                            if self.mouse_on_type == "grid_h" and self.mouse_on_num == row:
                                stack_c = np.vstack((stack_c, img_edit, border_w_highlighted))
                            else:
                                stack_c = np.vstack((stack_c, img_edit, border_w))
                    if self.mouse_on_type == "grid_v" and self.mouse_on_num == col:
                        stack = np.hstack((stack, stack_c, border_h_highlighted))
                    else:
                        stack = np.hstack((stack, stack_c, border_h))
            # Thin black border all over the image
            stack[-1:, :] = 0
            stack[:, -1:] = 0
            stack[:1, :] = 0
            stack[:, :1] = 0
            # Show Borders on image vertical(right side) and horizontal(bottom)
            if self.mouse_on_type == "border_h":
                stack[-2:, :] = self.highlight_color
            if self.mouse_on_type == "border_v":
                stack[:, -2:] = self.highlight_color
            # Show final image
            try:
                cv2.imshow("Edit", stack)
                # cv2.imshow("Edit", self.images[0][0])
            except:
                print('error!!: ', sys.exc_info()[0])

            # Quit if "q" pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.close_cv = True
            if cv2.getWindowProperty("Edit", cv2.WND_PROP_VISIBLE) < 1:
                self.close_cv = True
        cv2.destroyAllWindows()

    # Editing (move, scale) image
    def create_image(self, img, row, col, combined,  resize=True):
        # Local Variables
        border_top, border_bottom, border_left, border_right = 0, 0, 0, 0
        y, x = img.shape[:2]

        # Region coordinates to crop in world
        # If current row combined
        if combined == "rows":
            crop_x_start = int(x / 2 - width_total / zoom[row][col] / 2 - tr_x[row][col] / zoom[row][col])
            crop_x_end = int(crop_x_start + width_total / zoom[row][col])
            crop_y_start = int(y / 2 - cell_heights[row] / zoom[row][col] / 2 - tr_y[row][col] / zoom[row][col])
            crop_y_end = int(crop_y_start + cell_heights[row] / zoom[row][col])
        # If current column combined
        elif combined == "columns":
            crop_x_start = int(x / 2 - cell_widths[col] / zoom[row][col] / 2 - tr_x[row][col] / zoom[row][col])
            crop_x_end = int(crop_x_start + cell_widths[col] / zoom[row][col])
            crop_y_start = int(y / 2 - height_total / zoom[row][col] / 2 - tr_y[row][col] / zoom[row][col])
            crop_y_end = int(crop_y_start + height_total / zoom[row][col])
        # We have no combined rows or columns
        else:
            crop_x_start = int(x / 2 - cell_widths[col] / zoom[row][col] / 2 - tr_x[row][col] / zoom[row][col])
            crop_x_end = int(crop_x_start + cell_widths[col] / zoom[row][col])
            crop_y_start = int(y / 2 - cell_heights[row] / zoom[row][col] / 2 - tr_y[row][col] / zoom[row][col])
            crop_y_end = int(crop_y_start + cell_heights[row] / zoom[row][col])

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
        # Resize images
        if resize:
            if combined == "rows":
                img_edit = cv2.resize(img_edit, (width_total, cell_heights[row]),  interpolation=cv2.INTER_AREA)
            elif combined == "columns":
                img_edit = cv2.resize(img_edit, (cell_widths[col], height_total), interpolation=cv2.INTER_AREA)
            else:
                img_edit = cv2.resize(img_edit, (cell_widths[col], cell_heights[row]), interpolation=cv2.INTER_AREA)
        return img_edit

    # Editing (move, scale) image for save (higher resolution)
    def create_save_image(self, img, row, col, combined,  resize=True):

        # Create images without resize
        img_edit = self.create_image(img, row, col, combined, resize=False)

        # Resize with save resolution (1600px or smaller if images small)
        if resize:
            if combined == "rows":
                img_edit = cv2.resize(img_edit, (width_save_total, cell_save_heights[row]),  interpolation=cv2.INTER_AREA)
            elif combined == "columns":
                img_edit = cv2.resize(img_edit, (cell_save_widths[col], height_save_total), interpolation=cv2.INTER_AREA)
            else:
                img_edit = cv2.resize(img_edit, (cell_save_widths[col], cell_save_heights[row]), interpolation=cv2.INTER_AREA)
        return img_edit

    # Save Image
    def save_image_old(self, path):
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

    # Save Image
    def save_image(self, path):
        global cell_save_widths, cell_save_heights, width_save_total, height_save_total
        cell_scale_coefs = []

        # Calculation of a scale coefficients of all visible cells
        # If we don't have combined columns (Nothing combined or rows combined)
        if not any(combined_cols):
            # Loop all rows
            for row in range(num_of_rows):
                # If current row combined
                if combined_rows[row]:
                    img_edit = self.create_image(self.images[row][0], row, 0, combined="rows", resize=False)
                    cell_scale_coefs.append(img_edit.shape[0] / cell_heights[row])
                # If current row not combined
                else:
                    # Loop all cols
                    for col in range(num_of_cols):
                        img_edit = self.create_image(self.images[row][col], row, col, combined="none", resize=False)
                        cell_scale_coefs.append(img_edit.shape[0] / cell_heights[row])
        # If we have combined columns
        else:
            # Loop all columns
            for col in range(num_of_cols):
                # If current column combined
                if combined_cols[col]:
                    img_edit = self.create_image(self.images[0][col], 0, col, combined="cols", resize=False)
                    cell_scale_coefs.append(img_edit.shape[1] / cell_widths[col])
                # If current column not combined
                else:
                    # Loop all rows
                    for row in range(num_of_rows):
                        img_edit = self.create_image(self.images[row][col], row, col, combined="none", resize=False)
                        cell_scale_coefs.append(img_edit.shape[1] / cell_widths[col])
        # print(cell_scale_coefs)

        print(f"len(cell_widths): {len(cell_widths)}")
        print(f"len(cell_save_widths): {len(cell_save_widths)}")
        print(f"max(cell_scale_coefs): {max(cell_scale_coefs)}")

        # Calculation of global list vars "cell_save_widths[]" and "cell_save_heights[]"
        if width_total * max(cell_scale_coefs) < save_resolution_width:
            for i in range(len(cell_widths)):
                cell_save_widths[i] = int(cell_widths[i] * max(cell_scale_coefs))
            for i in range(len(cell_heights)):
                cell_save_heights[i] = int(cell_heights[i] * max(cell_scale_coefs))
        else:
            resolution_coef = save_resolution_width / width_total
            for i in range(len(cell_widths)):
                cell_save_widths[i] = int(cell_widths[i] * resolution_coef)
            for i in range(len(cell_heights)):
                cell_save_heights[i] = int(cell_heights[i] * resolution_coef)

        # Calculate global variables "width_save_total" and "height_save_total"
        width_save_total = 0
        for i in range(len(cell_save_widths)):
            width_save_total += cell_save_widths[i]
        height_save_total = 0
        for i in range(len(cell_save_heights)):
            height_save_total += cell_save_heights[i]

        # Stack Images
        # If we don't have combined columns
        if not any_col_combined:
            # print("ROWS")
            print("width_save_total: ", width_save_total)
            border_w = np.zeros((1, width_save_total + num_of_cols + 1, 3), dtype='uint8')
            stack = border_w.copy()
            for row in range(num_of_rows):
                # If current row combined
                if combined_rows[row]:
                    stack_r = self.create_save_image(self.images[row][0], row, 0, combined="rows")
                # If current row not combined
                else:
                    # Usual image border and highlighted border
                    border_h = np.zeros((cell_save_heights[row], 1, 3), dtype='uint8')
                    stack_r = border_h.copy()
                    # Loop all cols
                    for col in range(num_of_cols):
                        # Image creation
                        img_edit = self.create_save_image(self.images[row][col], row, col, combined="none")
                        # Adding border
                        stack_r = np.hstack((stack_r, img_edit, border_h))
                stack = np.vstack((stack, stack_r, border_w))

        # If we have combined columns
        else:
            # print("COLUMNS")
            border_h = np.zeros((height_save_total + num_of_rows, 1, 3), dtype='uint8')
            stack = border_h.copy()
            for col in range(num_of_cols):
                # If current column combined

                if combined_cols[col]:
                    stack_c = self.create_save_image(self.images[0][col], 0, col, combined="columns")
                # If current column not combined
                else:
                    # Usual image border and highlighted border
                    border_w = np.zeros((1, cell_save_widths[col], 3), dtype='uint8')
                    stack_c = border_w.copy()
                    # Loop all rows
                    for row in range(num_of_rows):
                        # Image creation
                        img_edit = self.create_save_image(self.images[row][col], row, col, combined="none")
                        # Adding usual or highlighted border
                        stack_c = np.vstack((stack_c, img_edit, border_w))
                stack = np.hstack((stack, stack_c, border_h))
        cv2.imwrite(path, stack)
        # Thin black border all over the image



        # if self.loop_type == 1:
        #     current_resolution = width1 / zoom[0]
        #     # Calculating resolution for save image
        #     if current_resolution < save_resolution:
        #         self.save_width1 = int(width1 / min(zoom))
        #         self.save_width2 = int(width2 / min(zoom))
        #         self.save_height1 = int(height1 / min(zoom))
        #         self.save_height2 = int(height2 / min(zoom))
        #     else:
        #         coefficient = 1600 / width1
        #         self.save_width1 = int(width1 * coefficient)
        #         self.save_width2 = int(width2 * coefficient)
        #         self.save_height1 = int(height1 * coefficient)
        #         self.save_height2 = int(height2 * coefficient)
        #
        #     self.set_base_save_resolution()
        #
        #     # Creating save images
        #     img_1_save = self.create_save_image(self.img_1, 0)
        #     stack = img_1_save
        #     # Stacking save images
        #     # border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
        #     # stack = np.hstack((img_1_save, border_h1, img_2_save))
        #     cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
        #                   (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)
        #     cv2.imwrite(path, stack)
        #
        # if self.loop_type == 2:
        #     current_resolution = (width1 + width2) / min(zoom[0], zoom[1])
        #     # Calculating resolution for save image
        #     if current_resolution < save_resolution:
        #         self.save_width1 = int(width1 / min(zoom))
        #         self.save_width2 = int(width2 / min(zoom))
        #         self.save_height1 = int(height1 / min(zoom))
        #         self.save_height2 = int(height2 / min(zoom))
        #     else:
        #         coefficient = 1600 / (width1 + width2)
        #         self.save_width1 = int(width1 * coefficient)
        #         self.save_width2 = int(width2 * coefficient)
        #         self.save_height1 = int(height1 * coefficient)
        #         self.save_height2 = int(height2 * coefficient)
        #
        #     self.set_base_save_resolution()
        #
        #     # Creating save images
        #     img_1_save = self.create_save_image(self.img_1, 0)
        #     img_2_save = self.create_save_image(self.img_2, 1)
        #
        #     # Stacking save images
        #     border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
        #     stack = np.hstack((img_1_save, border_h1, img_2_save))
        #     cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
        #                   (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)
        #
        #     cv2.imwrite(path, stack)

        # if self.loop_type == 6:
        #     current_resolution = (width1 + width2) / min(zoom)
        #     # Calculating resolution for save image
        #     if current_resolution < save_resolution:
        #         self.save_width1 = int(width1 / min(zoom))
        #         self.save_width2 = int(width2 / min(zoom))
        #         self.save_height1 = int(height1 / min(zoom))
        #         self.save_height2 = int(height2 / min(zoom))
        #     else:
        #         coefficient = 1600 / (width1 + width2)
        #         self.save_width1 = int(width1 * coefficient)
        #         self.save_width2 = int(width2 * coefficient)
        #         self.save_height1 = int(height1 * coefficient)
        #         self.save_height2 = int(height2 * coefficient)
        #
        #     self.set_base_save_resolution()
        #
        #     # Creating save images
        #     img_1_save = self.create_save_image(self.img_1, 0)
        #     img_2_save = self.create_save_image(self.img_2, 1)
        #     img_3_save = self.create_save_image(self.img_3, 2)
        #     img_4_save = self.create_save_image(self.img_4, 3)
        #
        #     # Stacking save images
        #     border_h1 = np.zeros((self.save_height1, 1, 3), dtype='uint8')
        #     stack1 = np.hstack((img_1_save, border_h1, img_2_save))
        #     border_h2 = np.zeros((self.save_height2, 1, 3), dtype='uint8')
        #     stack2 = np.hstack((img_3_save, border_h2, img_4_save))
        #     border_w = np.zeros((1, self.save_width1 + self.save_width2 + 1, 3), dtype='uint8')
        #     stack = np.vstack((stack1, border_w, stack2))
        #     cv2.rectangle(stack, (self.save_width1 - 1, self.save_height1 - 1),
        #                   (self.save_width1 + 1, self.save_height1 + 1), (100, 100, 100), -1)
        #
        #     cv2.imwrite(path, stack)

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
        global width_total, height_total, cell_widths, cell_heights
        if not self.resize:
            self.mouse_tile_position(x, y)
        # If Left Mouse Button Down
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.mouse_on_type == "cell":
                r, c = self.mouse_on_arr
                self.move = True
                self.start_x, self.start_y = x - tr_x[r][c], y - tr_y[r][c]
            else:
                self.resize = True
        # If Left Mouse Button Up
        elif event == cv2.EVENT_LBUTTONUP:
            self.resize = False
            self.move = False
        # If Mouse Move
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.move:
                r, c = self.mouse_on_arr
                tr_x[r][c], tr_y[r][c] = x - self.start_x, y - self.start_y
            if self.resize:
                # Resize Vertical Border
                if self.mouse_on_type == "border_v":
                    delta = int((x - width_total)/num_of_cols)
                    for i, cel in enumerate(cell_widths):
                        width = cell_widths[i] + delta
                        if width > 40:
                            cell_widths[i] = width
                    self.set_total_resolution()
                # Resize Vertical Grid
                elif self.mouse_on_type == "grid_v":
                    width = 1
                    for i in range(self.mouse_on_num + 1):
                        width += cell_widths[i] + 1
                    delta = x - width
                    width_left = cell_widths[i] + delta
                    width_right = cell_widths[i+1] - delta
                    if (width_left > 40) and (width_right > 40):
                        cell_widths[i] = width_left
                        cell_widths[i+1] = width_right
                    self.set_total_resolution()
                # Resize Horizontal Border
                elif self.mouse_on_type == "border_h":
                    delta = int((y - height_total)/num_of_rows)
                    # cell_heights = [y+delta for y in cell_heights]
                    for i, cel in enumerate(cell_heights):
                        height = cell_heights[i] + delta
                        if height > 40:
                            cell_heights[i] = height
                    self.set_total_resolution()
                # Resize Horizontal Grid
                elif self.mouse_on_type == "grid_h":
                    height = 1
                    for i in range(self.mouse_on_num + 1):
                        height += cell_heights[i] + 1
                    delta = y - height
                    height_top = cell_heights[i] + delta
                    height_bottom = cell_heights[i+1] - delta
                    if (height_top > 40) and (height_bottom > 40):
                        cell_heights[i] = height_top
                        cell_heights[i+1] = height_bottom
                    self.set_total_resolution()
        # If Mouse Wheel Scroll
        elif event == cv2.EVENT_MOUSEWHEEL:
            r, c = self.mouse_on_arr
            if flags > 0:
                zoom[r][c] *= 1.1
            else:
                zoom[r][c] /= 1.1

    # Function returns current tile number using mouse position
    # @staticmethod
    def mouse_tile_position(self, x, y):
        # Right Border
        if x > width_total - 9:
            self.mouse_on_type = "border_v"
            self.mouse_on_num = num_of_cols - 1
            return
        # Bottom Border
        if y > height_total - 9:
            self.mouse_on_type = "border_h"
            self.mouse_on_num = num_of_rows - 1
            return
        # Vertical Grid
        width = 1
        height = 1
        for i in range(num_of_cols-1):
            width += cell_widths[i] + 1
            if (width - 7) < x < (width + 7):
                if any_row_combined:
                    for a in range(num_of_rows):
                        height += cell_heights[a] + 1
                        if y < height:
                            if not combined_rows[a]:
                                self.mouse_on_type = "grid_v"
                                self.mouse_on_num = i
                            return
                    return
                else:
                    self.mouse_on_type = "grid_v"
                    self.mouse_on_num = i
                return
        # Horizontal Grid
        width = 1
        height = 1
        for i in range(num_of_rows-1):
            height += cell_heights[i] + 1
            if (height - 7) < y < (height + 7):
                if any_col_combined:
                    for a in range(num_of_cols):
                        width += cell_widths[a] + 1
                        if x < width:
                            if not combined_cols[a]:
                                self.mouse_on_type = "grid_h"
                                self.mouse_on_num = i
                            return
                    return
                else:
                    self.mouse_on_type = "grid_h"
                    self.mouse_on_num = i
                return
        # Cursor on Cell
        width = 1
        height = 1
        for r in range(num_of_rows):
            height += cell_heights[r] + 1
            if y < height:
                for c in range(num_of_cols):
                    width += cell_widths[c] + 1
                    if x < width:
                        self.mouse_on_type = "cell"
                        # print("type - cell")
                        if not self.move:
                            if combined_rows[r]:
                                self.mouse_on_arr = [r, 0]
                                return
                            if combined_cols[c]:
                                self.mouse_on_arr = [0, c]
                                return
                            self.mouse_on_arr = [r, c]
                            return
        # print("ERROR!")

    # Dimensions of multidimensional list
    def dim(self, a):
        if not type(a) == list:
            return []
        return [len(a)] + self.dim(a[0])

    # Close OpenCV
    def close_opencv(self):
        self.close_cv = True


# current_year = date.today().year
# if current_year < 2023:
# Global Variables
version = "1.1.0"
start_width = 900
start_height = 700
width_total = None
height_total = None
width_save_total = None
height_save_total = None
save_resolution_width = 1600
save_resolution_height = 1200
default_image_path = "./img/bg_image.png"

num_of_cols = None
num_of_rows = None
combined_rows = [False] * 7
combined_cols = [False] * 15
any_row_combined = False
any_col_combined = False


# Default Image Assignment
# Using: img_path[ROW][COLUMN]
rows, cols = (7, 15)
img_paths = [[default_image_path for i in range(cols)] for j in range(rows)]
zoom = [[1 for i in range(cols)] for j in range(rows)]
tr_x = [[0 for i in range(cols)] for j in range(rows)]
tr_y = [[0 for i in range(cols)] for j in range(rows)]
cell_widths = [0 for i in range(cols)]
cell_heights = [0 for i in range(rows)]
cell_save_widths = [0 for i in range(cols)]
cell_save_heights = [0 for i in range(rows)]
# Using: cell_sizes[AXIS(0-x,1-y)][ROW][COLUMN]
# cell_sizes = [[[0 for a in range(2)] for i in range(cols)] for j in range(rows)]

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
