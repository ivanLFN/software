from PyQt5.QtWidgets import QMainWindow
from ui_wnd import Ui_MainWindow
from widgets.header_widget import setup_header
from widgets.tab_widget import setup_tab_widget, StudyWidgetTab
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QMouseEvent, QRegion, QPainterPath
from connection import ConnectionAruino
from widgets.dialogs_windows import ResponseConnectionDialog
from database import DatabaseConnection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.ui.apply_settings.clicked.connect(self.set_settings_button)
        self.ui.check_connection.clicked.connect(self.check_connection_response)

        #Скругление углов
        self.setRoundCorners()


        # Инициализация заглолвка
        setup_header(self)

        # Инициализация браузера
        setup_tab_widget(self)

        # Соединение с портом Arduino
        self.connection = ConnectionAruino(self)

        self.draggable = False
        self.offset = QPoint()

        # База данных
        self.db_connection = DatabaseConnection()
        self.db_connection.fetch_data()
        self.db_connection.close_connection()

        # Графики на 2 вкладке
        self.dir_plots = StudyWidgetTab(self)




    def setRoundCorners(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

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

    def set_settings_button(self):
        self.connection.set_settings()

    def check_connection_response(self):
        response = self.connection.check_connection()
        dialog = ResponseConnectionDialog(response, self)
        dialog.exec_()
