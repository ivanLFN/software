from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from ui_dialog_wnd import Ui_Dialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class ResponseConnectionDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel(data)
        layout.addWidget(label)
        self.setLayout(layout)



class AddStudyDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()

        # Инициализация UI-элементов
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Настройка элементов диалогового окна
        self.ui.add_study_btn.clicked.connect(self.add_study)

        self.main_window = main_window

        self.ui.add_study_btn.setStyleSheet("""
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

        style_lineedit = """
            QLineEdit {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #2d6678;
                font-size: 16px;
                color: #161616;
                padding: 4px;
            }
        """

        self.ui.edit_x.setStyleSheet(style_lineedit)
        self.ui.edit_y.setStyleSheet(style_lineedit)
        self.ui.edit_z.setStyleSheet(style_lineedit)
        self.ui.edit_date.setStyleSheet(style_lineedit)
        self.ui.edit_desc.setStyleSheet(style_lineedit)
        self.ui.edit_title.setStyleSheet(style_lineedit)


    def add_study(self):
        # Обработка нажатия кнопки "Add"
        x = self.ui.edit_x.text()
        y = self.ui.edit_y.text()
        z = self.ui.edit_z.text()
        position = f"{x},{y},{z}"
        title = self.ui.edit_title.text()
        date = self.ui.edit_date.text()
        desc = self.ui.edit_desc.text()
        list_data = [title, position, date, desc]
        
        self.main_window.add_data_to_combobox(list_data)
        

        self.accept()
