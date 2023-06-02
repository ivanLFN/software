from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QMouseEvent, QRegion, QPainterPath, QPixmap, QIcon
import serial.tools.list_ports

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
            font-size: 22px;
            color: #161616;
        }
        
        QPushButton:hover {
            background-color: #2d6678;
        }
    """)

def add_available_ports(main_window):
    ports = serial.tools.list_ports.comports()
    port_list = [port.device for port in ports]

    for port in port_list:
        main_window.ui.COM.addItem(port)

