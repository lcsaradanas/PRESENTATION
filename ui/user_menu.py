from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGridLayout


class UserMainMenu(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None

    def set_user(self, user):
        self.user = user

    def setupUi(self, Widget):
        font_id = QtGui.QFontDatabase.addApplicationFont("myfont/ananda.ttf")
        if font_id != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Loaded font: {font_family}")
        else:
            print("Failed to load font")

        Widget.setObjectName("Widget")
        Widget.resize(1300, 800)

        self.widget = QtWidgets.QWidget(Widget)
        layout = QVBoxLayout(Widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.widget)

        self.widget.setStyleSheet("QWidget#widget { background-color: #9ecbf7; }")
        self.widget.setObjectName("widget")

        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(60, 60, 60, 60)
        self.main_layout.setSpacing(20)

        # Title
        self.title = QtWidgets.QLabel("Hi, USER!")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 36pt 'ananda'; color: black;")
        self.main_layout.addWidget(self.title)

        # Subtitle
        self.subtitle = QtWidgets.QLabel("What would you like to do?")
        self.subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle.setStyleSheet("font: 26pt 'Poppins'; color: black;")
        self.main_layout.addWidget(self.subtitle)

        # Options Container
        self.options_container = QtWidgets.QWidget()
        self.options_container.setMinimumSize(900, 350)
        self.options_container.setStyleSheet("background-color: #f9f7b6; border-radius: 30px;")

        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(100, 100, 100, 100)
        self.options_layout.setSpacing(50)

        # ORGANIZATION Row
        org_row = QHBoxLayout()
        self.org_label = QtWidgets.QLabel("ORGANIZATION")
        self.org_label.setStyleSheet("font: bold 22pt 'Poppins'; color: black;")
        org_row.addWidget(self.org_label)

        org_row.addStretch()

        self.edit_info_button = QtWidgets.QPushButton("EDIT INFO")
        self.edit_info_button.setFixedSize(220, 60)
        self.edit_info_button.setStyleSheet("""
            QPushButton {
                background-color: #bcd8a3;
                font: bold 16pt 'Poppins';
                border: 2px solid green;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #a5c48e;
            }
        """)
        org_row.addWidget(self.edit_info_button)
        self.options_layout.addLayout(org_row)

        # DELIVERY Row
        del_row = QHBoxLayout()
        self.del_label = QtWidgets.QLabel("DELIVERY")
        self.del_label.setStyleSheet("font: bold 22pt 'Poppins'; color: black;")
        del_row.addWidget(self.del_label)

        del_row.addStretch()

        self.view_button = QtWidgets.QPushButton("VIEW")
        self.view_button.setFixedSize(220, 60)
        self.view_button.setStyleSheet("""QPushButton {background-color: #f5c2c7; font: bold 16pt 'Poppins'; border: 2px solid purple; border-radius: 30px;}
            QPushButton:hover {background-color: #e8b2ba;}""")
        del_row.addWidget(self.view_button)
        self.options_layout.addLayout(del_row)

        # Add options container to main layout with vertical stretch
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.options_container, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addStretch(1)

        # LOGOUT Button
        self.logout_btn = QtWidgets.QPushButton("LOG OUT")
        self.logout_btn.setFixedSize(180, 55)
        self.logout_btn.setStyleSheet("""QPushButton {background-color: #f5a89c; font: bold 14pt 'Poppins'; border: 2px solid red; border-radius: 22px; padding: 10px 20px;}
            QPushButton:hover {background-color: #e89688;}""")
        self.main_layout.addWidget(self.logout_btn, alignment=QtCore.Qt.AlignCenter)

        # Button Connections
        self.edit_info_button.clicked.connect(self.open_edit_personal_info)
        self.view_button.clicked.connect(self.open_view_delivery)
        self.logout_btn.clicked.connect(self.logout)

    def logout(self):
        self.main_window.show_welcome_screen()

    def open_edit_personal_info(self):
        self.main_window.show_edit_personal_info(self.user)

    def open_view_delivery(self):
        self.main_window.show_view_delivery_user(self.user)
