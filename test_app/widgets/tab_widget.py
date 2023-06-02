from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt
import serial.tools.list_ports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import threading
import time
import math


def setup_tab_widget(main_window):

    pixmap_1 = QPixmap("static/img/pref.png")
    pref_pixmap = QIcon(pixmap_1)
    main_window.ui.tabWidget.setTabIcon(0, pref_pixmap)

    pixmap_2 = QPixmap("static/img/new_study.png")
    pref_pixmap = QIcon(pixmap_2)
    main_window.ui.tabWidget.setTabIcon(1, pref_pixmap)



    add_available_ports(main_window)


    main_window.ui.apply_settings.setStyleSheet("""
        QPushButton {
            background-color: #f9f9f9;
            border-radius: 10px;
            border: 1px solid #2d6678;
            font-size: 22px;
            color: #161616;
        }
        
        QPushButton:hover {
            background-color: #2d6678;
        }
    """)

    main_window.ui.check_connection.setStyleSheet("""
        QPushButton {
            background-color: #f9f9f9;
            border-radius: 10px;
            border: 1px solid #2d6678;
            font-size: 22px;
            color: #161616;
        }
        
        QPushButton:hover {
            background-color: #2d6678;
        }
    """)

    main_window.ui.checkBox_showplot.setStyleSheet('''
         QCheckBox {
        spacing: 5px;
        font-size: 18px;
        color: #333333;
        }
        
        QCheckBox::indicator {
            width: 30px;
            height: 20px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #455a64;
            background-color: white;
            border-radius: 10px;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #455a64;
            background-color: #2d6577;
            border-radius: 10px;
        }
    ''')    

    
def add_available_ports(main_window):
    ports = serial.tools.list_ports.comports()
    port_list = [port.device for port in ports]

    for port in port_list:
        main_window.ui.COM.addItem(port)


class StudyWidgetTab():
    def __init__(self, main_window):

        self.main_window = main_window

        main_window.ui.checkBox_showplot.stateChanged.connect(self.handle_checkBox_stateChanged)
        
        self.flag_stopped = True

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

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.main_window.ui.widget.setLayout(plot_layout)


    def run_thread(self):
        while self.flag_stopped:
            self.update_graph()  # Вызов метода
            time.sleep(1)  # Приостановка выполнения на 1 секунду


    def update_graph(self):
        # Генерация случайных данных для осей x, y, z (замените этот код на ваш код получения данных)
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        z = np.random.randint(0, 100)

        # Добавление новых данных в списки
        x, y, z = self.calculate_rotation_angles()

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

    
    def handle_checkBox_stateChanged(self, state):
        if state == Qt.Checked:
            # self.start_timer()
            self.flag_stopped = True
            self.thread = threading.Thread(target=self.run_thread)
            self.thread.start()
        else:
            # self.timer_turn_off()
            self.flag_stopped = False


    def calculate_rotation_angles(self):

        # Получение данных от arduino как tuple
        data_tuple = self.main_window.connection.get_data()

        # Вычисление углов на основе акселерометра
        roll_acc = math.atan2(data_tuple[4], data_tuple[5]) * 180 / math.pi
        pitch_acc = math.atan2(-data_tuple[3], math.sqrt(data_tuple[4] * data_tuple[4] + data_tuple[5] * data_tuple[5])) * 180 / math.pi

        # Вычисление углов на основе гироскопа
        dt = 1.0  # Интервал времени между обновлениями (в секундах)
        gyro_x = data_tuple[0] * dt
        gyro_y = data_tuple[1] * dt
        gyro_z = data_tuple[2] * dt

        roll = gyro_x + roll_acc
        pitch = gyro_y + pitch_acc
        yaw = gyro_z

        return roll, pitch, yaw