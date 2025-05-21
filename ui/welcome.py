from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class WelcomeScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1301, 811)

        # Main widget with background - fill the entire parent widget
        self.widget = QtWidgets.QWidget(Widget)

        # Use a layout for the parent Widget to ensure the background fills everything
        layout = QVBoxLayout(Widget)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins to ensure full coverage
        layout.setSpacing(0)
        layout.addWidget(self.widget)

        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(158, 198, 243);}")
        self.widget.setObjectName("widget")

        # Main vertical layout for the widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        # Add spacer at the top
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Welcome text (horizontal layout for centering)
        self.welcome_layout = QHBoxLayout()
        self.welcome_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 78pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("WELCOME")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.welcome_layout.addWidget(self.label)
        self.welcome_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.welcome_layout)

        # Subtitle text (horizontal layout for centering)
        self.subtitle_layout = QHBoxLayout()
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("font: 18pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Donation Drive System")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.subtitle_layout.addWidget(self.label_2)
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.subtitle_layout)

        # Add spacer between title and buttons
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Login button (horizontal layout for centering)
        self.login_layout = QHBoxLayout()
        self.login_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.login_button = QtWidgets.QPushButton()
        self.login_button.setMinimumSize(QtCore.QSize(391, 61))
        self.login_button.setMaximumSize(QtCore.QSize(500, 61))
        self.login_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color:rgb(255, 225, 189);
                font: 75 14pt "Century Gothic";
                border: 2px solid orange;
            }
            QPushButton:hover {
                background-color: rgb(240, 200, 150);
            }
        """)
        self.login_button.setObjectName("login_button")
        self.login_button.setText("LOGIN")

        self.login_layout.addWidget(self.login_button)
        self.login_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.login_layout)

        # Add small spacer between buttons
        self.main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Signup button (horizontal layout for centering)
        self.signup_layout = QHBoxLayout()
        self.signup_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.signup_button = QtWidgets.QPushButton()
        self.signup_button.setMinimumSize(QtCore.QSize(391, 61))
        self.signup_button.setMaximumSize(QtCore.QSize(500, 61))
        self.signup_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #BBD8A3;
                color: black;
                font: 75 14pt "Century Gothic";
                border: 2px solid green;
            }
            QPushButton:hover {
                background-color: #A6C18F;
            }
        """)
        self.signup_button.setObjectName("signup_button")
        self.signup_button.setText("SIGN UP")

        self.signup_layout.addWidget(self.signup_button)
        self.signup_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.signup_layout)

        # Add spacer at the bottom
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Connect the buttons to their functions
        self.login_button.clicked.connect(self.open_login)
        self.signup_button.clicked.connect(self.open_signup)

        # Handle window resize events
        Widget.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Handle window resize events"""
        # This method is called when the window is resized
        # The layouts will automatically adjust the widgets
        # No need to call super as we're not a true QWidget subclass
        pass

    def open_login(self):
        # Switch to login screen
        self.main_window.show_login_screen()

    def open_signup(self):
        # Switch to create account screen
        self.main_window.show_create_account_screen()