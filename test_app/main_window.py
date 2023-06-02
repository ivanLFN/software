from PyQt5.QtWidgets import QMainWindow, QLabel
from ui_wnd import Ui_MainWindow
from widgets.header_widget import setup_header
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Инициализация заглолвка
        setup_header(self) 

        

    
        self.draggable = False
        self.offset = QPoint()


    def close_application(self):
        self.close()

    def minimize_application(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.showMinimized()
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and event.pos() in self.ui.header_widget.geometry():
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggable and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draggable = False



    