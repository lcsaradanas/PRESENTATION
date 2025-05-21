from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class ViewAdminsScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.admin_accounts = []

    def set_user(self, user):
        self.user = user
        self.load_admin_accounts()

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
        self.main_layout.setContentsMargins(40, 20, 40, 20)
        self.main_layout.setSpacing(10)

        # Title area
        self.title_layout = QHBoxLayout()

        # Add spacer to center the title
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Title
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 30pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("VIEW ADMIN ACCOUNTS")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.title_layout.addWidget(self.label)
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout.addLayout(self.title_layout)

        # Admin List Label
        self.list_label = QtWidgets.QLabel()
        self.list_label.setStyleSheet("font: 18pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.list_label.setAlignment(QtCore.Qt.AlignCenter)
        self.list_label.setObjectName("list_label")
        self.list_label.setText("List of All Admins")
        self.list_label.setMaximumHeight(41)

        self.main_layout.addWidget(self.list_label)

        # Search Layout
        self.search_layout = QHBoxLayout()

        # "SEARCH:" Label
        self.search_label = QtWidgets.QLabel("SEARCH:")
        self.search_label.setStyleSheet("font: 12pt 'Century Gothic'; color: #4c6b8c;")
        self.search_layout.addWidget(self.search_label)

        # Search Input Field
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText("Enter username or name")
        self.search_layout.addWidget(self.search_field)

        # Search Button
        self.search_button = QtWidgets.QPushButton("SEARCH")
        self.search_button.setMinimumWidth(120)
        self.search_button.setStyleSheet("""
                   QPushButton {
                       border-radius: 10px;
                       background-color: rgb(187, 216, 163);
                       font: 75 12pt 'Century Gothic';
                       border: 2px solid green;
                   }
                   QPushButton:hover {
                       background-color: rgb(167, 201, 140);
                   }
               """)
        self.search_layout.addWidget(self.search_button)

        # Add the search layout to the main layout
        self.main_layout.addLayout(self.search_layout)

        # Table widget for admin accounts
        self.table = QtWidgets.QTableWidget()
        self.table.setObjectName("admin_table")
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Username", "First Name", "Last Name"])

        # Set the table style
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                border: 1px solid #76a5af;
                border-radius: 8px;
                selection-background-color: #a6c9e2;
            }
            QHeaderView::section {
                background-color: #d0e8eb;
                border: 1px solid #76a5af;
                padding: 4px;
                font-weight: bold;
            }
        """)

        # Set columns to stretch
        header = self.table.horizontalHeader()
        for col in range(3):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        # Add table to main layout
        self.main_layout.addWidget(self.table, 1)  # 1 is the stretch factor

        # Button area
        self.button_layout = QHBoxLayout()
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Back button
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setMinimumSize(QtCore.QSize(161, 61))
        self.back_button.setMaximumSize(QtCore.QSize(161, 61))
        self.back_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color:rgb(255, 225, 189);
                font: 75 14pt "Century Gothic";
                border: 2px solid orange;
            }
            QPushButton:hover {
                background-color: rgb(240, 200, 150);
            }
        """)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")

        self.button_layout.addWidget(self.back_button)
        self.main_layout.addLayout(self.button_layout)

        # Connect buttons
        self.back_button.clicked.connect(self.go_back)
        self.search_button.clicked.connect(self.apply_search)

        # Handle window resize events
        Widget.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Handle window resize events"""
        # This method is called when the window is resized
        # The layouts will automatically adjust the widgets
        # No need to call super as we're not a true QWidget subclass
        pass

    def search_admin_accounts(self, term):
        query = """
                SELECT * \
                FROM admin_accounts
                WHERE username LIKE ? \
                   OR firstname LIKE ? \
                   OR lastname LIKE ? \
                """
        wildcard_term = f"%{term}%"
        return self.execute(query, (wildcard_term, wildcard_term, wildcard_term)).fetchall()

    def load_admin_accounts(self, search_term=None):
        """Load admin accounts from the database"""
        if not self.user:
            return

        # Get all admin accounts
        self.admin_accounts = self.database.get_all_admin_accounts()

        # Clear existing table rows
        self.table.setRowCount(0)

        # Get all or filtered admin accounts
        if search_term:
            self.admin_accounts = self.database.search_admin_accounts(search_term)
        else:
            self.admin_accounts = self.database.get_all_admin_accounts()

        self.table.setRowCount(0)

        # Populate the table
        for row, admin in enumerate(self.admin_accounts):
            # The database query returns user_code, username, firstname, lastname
            username = admin[1]
            firstname = admin[2]
            lastname = admin[3]

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(username))
            self.table.setItem(row, 1, QTableWidgetItem(firstname))
            self.table.setItem(row, 2, QTableWidgetItem(lastname))


    def apply_search(self):
        search_term = self.search_field.text()
        self.load_admin_accounts(search_term=search_term)

    def go_back(self):
        """Go back to the main menu"""
        if self.user and self.user[6]:  # User is admin
            self.main_window.show_admin_menu(self.user)
        else:
            self.main_window.show_welcome_screen()