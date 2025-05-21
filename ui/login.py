from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class LoginScreen(object):
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
                                  "background-color:rgb(158, 198, 243);}\n"
                                  "QLineEdit {\n"
                                  "background-color: white;\n"
                                  "}")
        self.widget.setObjectName("widget")

        # Main vertical layout for the widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        # Add spacer at the top
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Login title (horizontal layout for centering)
        self.title_layout = QHBoxLayout()
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 78pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("L O G I N")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.title_layout.addWidget(self.label)
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.title_layout)

        # Subtitle (horizontal layout for centering)
        self.subtitle_layout = QHBoxLayout()
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("font: 18pt \"Lemon/Milk\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Log in to your existing account")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.subtitle_layout.addWidget(self.label_2)
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.subtitle_layout)

        # Add spacer between title and form fields
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Form container (to center the form fields)
        self.form_container = QHBoxLayout()
        self.form_container.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Form fields layout
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)

        # Username label
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("USERNAME")
        self.form_layout.addWidget(self.label_3)

        # Username field
        self.userfield = QtWidgets.QLineEdit()
        self.userfield.setMinimumSize(QtCore.QSize(421, 41))
        self.userfield.setMaximumSize(QtCore.QSize(600, 41))
        self.userfield.setObjectName("userfield")
        self.form_layout.addWidget(self.userfield)

        # Add small spacer between fields
        self.form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Password label
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("PASSWORD")
        self.form_layout.addWidget(self.label_4)

        # Password field
        self.passwordfield = QtWidgets.QLineEdit()
        self.passwordfield.setMinimumSize(QtCore.QSize(421, 41))
        self.passwordfield.setMaximumSize(QtCore.QSize(600, 41))
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordfield.setObjectName("passwordfield")
        self.form_layout.addWidget(self.passwordfield)

        # Add small spacer after password field
        self.form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Error message
        self.error1 = QtWidgets.QLabel()
        self.error1.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        # Ensure the error message starts empty
        self.error1.setText("")
        self.error1.setObjectName("error1")
        self.error1.setAlignment(QtCore.Qt.AlignCenter)
        self.form_layout.addWidget(self.error1)

        # Add button spacer
        self.form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Login button
        self.login = QtWidgets.QPushButton()
        self.login.setMinimumSize(QtCore.QSize(391, 61))
        self.login.setMaximumSize(QtCore.QSize(600, 61))
        self.login.setStyleSheet("""
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
        self.login.setObjectName("login")
        self.login.setText("LOG IN")
        self.form_layout.addWidget(self.login)

        # Add small spacer between buttons
        self.form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Back button
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setMinimumSize(QtCore.QSize(391, 61))
        self.back_button.setMaximumSize(QtCore.QSize(600, 61))
        self.back_button.setStyleSheet("""
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
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")
        self.form_layout.addWidget(self.back_button)

        # Add the form layout to the container with spacers for centering
        self.form_container.addLayout(self.form_layout)
        self.form_container.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Add the form container to the main layout
        self.main_layout.addLayout(self.form_container)

        # Add spacer at the bottom
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Connect the login button to login function
        self.login.clicked.connect(self.login_function)
        self.back_button.clicked.connect(self.go_back)

        # Clear any error messages when form loads
        self.error1.clear()

        # Clear error message when user starts typing
        self.userfield.textChanged.connect(self.clear_error)
        self.passwordfield.textChanged.connect(self.clear_error)

        # Handle window resize events
        Widget.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Handle window resize events"""
        # This method is called when the window is resized
        # The layouts will automatically adjust the widgets
        # No need to call super as we're not a true QWidget subclass
        pass

    def login_function(self):
        username = self.userfield.text()
        password = self.passwordfield.text()

        # Only show validation error if the login button was actually clicked
        if not username or not password:
            self.error1.setText("Please fill in all fields")
            return

        user = self.database.verify_login(username, password)

        if user:
            self.open_main_menu(user)
            # Clear fields after successful login
            self.userfield.clear()
            self.passwordfield.clear()
            self.error1.setText("")
        else:
            self.error1.setText("Invalid username or password")

    def go_back(self):
        # Go back to welcome screen
        self.main_window.show_welcome_screen()

    def open_main_menu(self, user):
        # Check if user is admin or regular user
        if user[6]:  # typeOfUser is True (admin)
            # Show admin menu
            self.main_window.show_admin_menu(user)
        else:
            # Show user menu
            self.main_window.show_user_menu(user)

    def clear_error(self):
        """Clear error message when user interacts with the form"""
        self.error1.setText("") 