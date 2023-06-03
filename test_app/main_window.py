from PyQt5.QtWidgets import QMainWindow, QDialog
from ui_wnd import Ui_MainWindow
from widgets.header_widget import setup_header
from widgets.tab_widget import setup_tab_widget, StudyWidgetTab
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QMouseEvent, QRegion, QPainterPath
from connection import ConnectionAruino
from widgets.dialogs_windows import ResponseConnectionDialog
from database import DatabaseConnection
from widgets.dialogs_windows import AddStudyDialog
import time



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.ui.apply_settings.clicked.connect(self.set_settings_button)
        self.ui.check_connection.clicked.connect(self.check_connection_response)
        self.ui.mode_combobox.currentIndexChanged.connect(self.update_text_browser)
        self.ui.add_mode.clicked.connect(self.open_add_data_dialog)
        self.ui.clear_btn.clicked.connect(self.clear_text_edit)

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
        self.add_data_to_combobox()
        
        # self.db_connection.close_connection()



        # Графики на 2 вкладке
        self.dir_plots = StudyWidgetTab(self)


        self.pritn_to_console("Application launched [OK]")


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

    def add_data_to_combobox(self, list_param=None):
        self.db_connection.create_table()

        if list_param:
            self.db_connection.insert_data(list_param[0], list_param[1], list_param[2], list_param[3])

        self.list_study = self.db_connection.fetch_all_data()

        self.ui.mode_combobox.clear()
        
        for item in self.list_study:
            self.ui.mode_combobox.addItem(item[1])
    
    def update_text_browser(self, index):
        selected_item = self.list_study[index]
        text = f"Дополнительные данные:\n"
        text += f"Параметры: {selected_item[2]}\n"
        text += f"Дата: {selected_item[3]}\n"
        text += f"Описание: {selected_item[4]}\n"
        self.ui.textBrowser.setText(text)

    def open_add_data_dialog(self):
        dialog = AddStudyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pass

    def clear_text_edit(self):
        self.ui.textEdit.clear()

    def pritn_to_console(self, text_print):
        total_line = '[' + time.ctime() + ': ' + text_print + ']'
        self.ui.textEdit.append(total_line)