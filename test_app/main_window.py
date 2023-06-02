from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from ui_wnd import Ui_MainWindow
from widgets.header_widget import setup_header
from widgets.tab_widget import setup_tab_widget
from PyQt5.QtCore import Qt, QPoint, QRectF, QTimer
from PyQt5.QtGui import QMouseEvent, QRegion, QPainterPath, QPixmap, QIcon
from connection import ConnectionAruino
from widgets.dialogs_windows import ResponseConnectionDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
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
        db_connection = DatabaseConnection()
        db_connection.insert_data("9.81,-0.32,9.45,-120,50,80")
        db_connection.fetch_data()
        db_connection.close_connection()



        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.subplots(3, 1)

        self.axes[0].set_ylabel('X')
        self.axes[1].set_ylabel('Y')
        self.axes[2].set_ylabel('Z')
        self.axes[2].set_xlabel('Time')

        self.canvas.draw()

        self.data_x = []
        self.data_y = []
        self.data_z = []

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Интервал обновления в миллисекундах
        self.timer.timeout.connect(self.update_graph)
        self.timer.start()

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.ui.widget.setLayout(plot_layout)



    def update_graph(self):
        # Генерация случайных данных для осей x, y, z (замените этот код на ваш код получения данных)
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        z = np.random.randint(0, 100)

        # Добавление новых данных в списки
        self.data_x.append(x)
        self.data_y.append(y)
        self.data_z.append(z)

        self.data_x = self.data_x[-50:]
        self.data_y = self.data_y[-50:]
        self.data_z = self.data_z[-50:]

        # Очистка графиков и отображение новых данных
        self.axes[0].clear()
        self.axes[1].clear()
        self.axes[2].clear()
        
        self.axes[0].plot(self.data_x)
        self.axes[1].plot(self.data_y)
        self.axes[2].plot(self.data_z)

        self.canvas.draw()









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
