from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QLabel, QPushButton


class ResponseConnectionDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel(data)
        layout.addWidget(label)
        self.setLayout(layout)