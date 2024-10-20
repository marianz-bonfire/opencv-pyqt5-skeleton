import sys
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt

from widgets.SourceView import SourceView
from widgets.StackedListWidgets import ScreenListWidget
from widgets.CameraView import CameraView

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.tool_bar = self.addToolBar('Toolbar')
        self.action_right_rotate = QAction(QIcon("icons/rotate_right.png"), "Rotate to the right 90", self)
        self.action_left_rotate = QAction(QIcon("icons/rotate_left.png"), "Rotate to the left 90°", self)
        self.action_histogram = QAction(QIcon("icons/histogram.png"), "Histogram", self)
        self.action_right_rotate.triggered.connect(self.right_rotate)
        self.action_left_rotate.triggered.connect(self.left_rotate)
        self.action_histogram.triggered.connect(self.histogram)
        self.tool_bar.addActions((self.action_left_rotate, self.action_right_rotate, self.action_histogram))

        self.screenListWidget = ScreenListWidget(self)
        self.sourceView = SourceView(self)
        self.cameraView = CameraView(self)

        self.dock_source = QDockWidget(self)
        self.dock_source.setWidget(self.sourceView)
        self.dock_source.setTitleBarWidget(QLabel('Source'))
        self.dock_source.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_screens = QDockWidget(self)
        self.dock_screens.setWidget(self.screenListWidget)
        self.dock_screens.setTitleBarWidget(QLabel('Screens'))
        self.dock_screens.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.setCentralWidget(self.cameraView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_source)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_screens)

        self.setWindowTitle('PyQt5 + OpenCV Video Processing')
        self.setWindowIcon(QIcon('icons/main.png'))
        self.src_img = None
        self.cur_img = None


        #Initialize cameras
        self.init_cameras()

    def init_cameras(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_capture)
        self.timer.start(27)

    def update_capture(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            self.src_img = frame
            self.update_image()
        else:
            pass

    def update_image(self):
        if self.src_img is None:
            return
        img = self.process_image()
        self.cur_img = img
        self.cameraView.update_image(img)

    def change_image(self, img):
        self.src_img = img
        img = self.process_image()
        self.cur_img = img
        self.cameraView.change_image(img)

    def process_image(self):
        img = self.src_img.copy()
        for i in range(self.screenListWidget.count()):
            img = self.screenListWidget.item(i)(img)
        return img

    def right_rotate(self):
        self.cameraView.rotate(90)

    def left_rotate(self):
        self.cameraView.rotate(-90)

    def histogram(self):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([self.cur_img], [i], None, [256], [0, 256])
            histr = histr.flatten()
            plt.plot(range(256), histr, color=col)
            plt.xlim([0, 256])
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open('styles/styleSheet.qss', encoding='utf-8').read())
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
