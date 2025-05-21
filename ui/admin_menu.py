from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGridLayout

class AdminMainMenu(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None

    def set_user(self, user):
        self.user = user

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1287, 810)

        # Main widget with background - fill the entire parent widget
        self.widget = QtWidgets.QWidget(Widget)

        # Use a layout for the parent Widget to ensure the background fills everything
        layout = QVBoxLayout(Widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.widget)

        self.widget.setStyleSheet("background-color: #ADD8E6;")
        self.widget.setObjectName("widget")

        # Main layout for the widget - using a Grid Layout for better control
        self.main_layout = QGridLayout(self.widget)
        self.main_layout.setContentsMargins(60, 30, 60, 30)

        # Header
        header = QtWidgets.QLabel("WHAT WOULD YOU LIKE TO DO?")
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("font: bold 32pt 'Century Gothic'; background-color: #FFFFCC; color: black; border-radius: 20px; border: 2px solid gold;")
        self.main_layout.addWidget(header, 0, 0, 1, 4)

        # Section headers
        sections = ["CREATE", "EDIT", "DELETE", "VIEW"]
        for i, title in enumerate(sections):
            label = QtWidgets.QLabel(title)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("font: bold 24pt 'Century Gothic'; color: black;")
            self.main_layout.addWidget(label, 1, i)

        # Button styles
        style_create = (
            "QPushButton {background-color: #FFD9A0; font: bold 14pt 'Century Gothic'; "
            "border: 2px solid orange; border-radius: 15px;}"
            "QPushButton:hover {background-color: #FFC577; border: 2px solid darkorange;}"
        )

        style_edit = (
            "QPushButton {background-color: #FEFFA5; font: bold 14pt 'Century Gothic'; "
            "border: 2px solid gold; border-radius: 15px;}"
            "QPushButton:hover {background-color: #F6F86C; border: 2px solid goldenrod;}"
        )

        style_delete = (
            "QPushButton {background-color: #FBCDEB; font: bold 14pt 'Century Gothic'; "
            "border: 2px solid purple; border-radius: 15px;}"
            "QPushButton:hover {background-color: #F8A6D9; border: 2px solid darkmagenta;}"
        )

        style_view = (
            "QPushButton {background-color: #BBD8A3; font: bold 14pt 'Century Gothic'; "
            "border: 2px solid green; border-radius: 15px;}"
            "QPushButton:hover {background-color: #A7C98C; border: 2px solid darkgreen;}"
        )

        style_logout = (
            "QPushButton {background-color: #F7AFAF; font: bold 14pt 'Century Gothic'; "
            "border: 2px solid red; border-radius: 15px;}"
            "QPushButton:hover {background-color: #F08080; border: 2px solid darkred;}"
        )

        # CREATE buttons
        self.main_layout.addWidget(self.makeButton("PRODUCTS", style_create, self.open_add_products), 2, 0)
        self.main_layout.addWidget(self.makeButton("DELIVERY", style_create, self.open_add_delivery), 3, 0)

        # EDIT buttons
        self.main_layout.addWidget(self.makeButton("PRODUCTS", style_edit, self.open_edit_products), 2, 1)
        self.main_layout.addWidget(self.makeButton("DELIVERY", style_edit, self.open_edit_delivery), 3, 1)

        # DELETE buttons
        self.main_layout.addWidget(self.makeButton("PRODUCTS", style_delete, self.open_delete_products), 2, 2)
        self.main_layout.addWidget(self.makeButton("DELIVERY", style_delete, self.open_delete_delivery), 3, 2)

        # VIEW buttons
        self.main_layout.addWidget(self.makeButton("PRODUCTS", style_view, self.open_view_products), 2, 3)
        self.main_layout.addWidget(self.makeButton("DELIVERY", style_view, self.open_view_delivery), 3, 3)
        self.main_layout.addWidget(self.makeButton("ORGANIZATION", style_view, self.open_view_organization), 4, 3)
        self.main_layout.addWidget(self.makeButton("ADMINS", style_view, self.open_view_admins), 5, 3)

        # Logout button
        self.logout_btn = QtWidgets.QPushButton("LOGOUT")
        self.logout_btn.setStyleSheet("""QPushButton {background-color: #f5a89c; font: bold 14pt 'Poppins'; border: 2px solid red; border-radius: 22px; padding: 10px 20px;}
            QPushButton:hover {background-color: #e89688;}""")
        self.logout_btn.setFixedWidth(150)
        self.main_layout.addWidget(self.logout_btn, 5, 0, 1, 1)
        self.logout_btn.clicked.connect(self.logout)

    def makeButton(self, text, style, func):
        btn = QtWidgets.QPushButton(text)
        btn.setStyleSheet(style)
        btn.setMinimumSize(QtCore.QSize(180, 100))
        btn.clicked.connect(func)
        return btn

    def logout(self):
        self.main_window.show_welcome_screen()

    def open_add_products(self):
        self.main_window.show_add_products(self.user)

    def open_add_delivery(self):
        self.main_window.show_add_delivery(self.user)

    def open_delete_products(self):
        self.main_window.show_delete_products(self.user)

    def open_delete_delivery(self):
        self.main_window.show_delete_delivery(self.user)

    def open_edit_products(self):
        self.main_window.show_edit_products(self.user)

    def open_edit_delivery(self):
        self.main_window.show_edit_delivery(self.user)

    def open_view_products(self):
        self.main_window.show_view_products(self.user)

    def open_view_delivery(self):
        self.main_window.show_view_delivery(self.user)

    def open_view_organization(self):
        self.main_window.show_view_organization(self.user)

    def open_view_admins(self):
        self.main_window.show_view_admins(self.user)
