
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication([])

    # Создание и отображение главного окна
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())