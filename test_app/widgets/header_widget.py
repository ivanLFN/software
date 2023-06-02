from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


def setup_header(main_window):

    header_pixmap = QPixmap("static/img/header_img.png")
    main_window.ui.header_img.setPixmap(header_pixmap)


    logo_img = QPixmap("static/img/logo.png")
    scaled_logo_img = logo_img.scaled(main_window.ui.logo.size(), Qt.AspectRatioMode.KeepAspectRatio)
    main_window.ui.logo.setPixmap(scaled_logo_img)



    minimize_pixmap = QPixmap("static/img/minimize.png")
    main_window.ui.minimize_btn.setPixmap(minimize_pixmap)
    main_window.ui.minimize_btn.setAlignment(Qt.AlignCenter)
    main_window.ui.minimize_btn.mousePressEvent = main_window.minimize_application

    close_pixmap = QPixmap("static/img/close.png")
    main_window.ui.close_btn.setPixmap(close_pixmap)
    main_window.ui.close_btn.setAlignment(Qt.AlignCenter)
    main_window.ui.close_btn.mousePressEvent = main_window.close_application




    

