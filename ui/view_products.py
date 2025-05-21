from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class ViewProductsScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.food_lists = []

    def set_user(self, user):
        self.user = user
        self.load_food_lists()

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
        self.label.setText("VIEW PRODUCTS")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.title_layout.addWidget(self.label)
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout.addLayout(self.title_layout)

        # Products List Label
        self.list_label = QtWidgets.QLabel()
        self.list_label.setStyleSheet("font: 18pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.list_label.setObjectName("list_label")
        self.list_label.setText("Products List:")
        self.list_label.setMaximumHeight(41)

        self.main_layout.addWidget(self.list_label)

        # Tab widget for food lists
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #76a5af;
                background: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #d0e8eb;
                border: 1px solid #76a5af;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
        """)

        self.main_layout.addWidget(self.tab_widget, 1)  # 1 is the stretch factor

        # Button area
        self.button_layout = QHBoxLayout()
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # OK button
        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setMinimumSize(QtCore.QSize(161, 61))
        self.ok_button.setMaximumSize(QtCore.QSize(161, 61))
        self.ok_button.setStyleSheet("""
            QPushButton { 
                border-radius: 20px;   
                background-color: #BBD8A3;
                font: 75 16pt "Century Gothic";
                color: black;
                border: 2px solid green;
            }
            QPushButton:hover {
                background-color: #A6C18F;
            }
        """)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setText("OK")

        self.button_layout.addWidget(self.ok_button)
        self.main_layout.addLayout(self.button_layout)

        # Connect buttons
        self.ok_button.clicked.connect(self.go_back)

        # Handle window resize events
        Widget.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Handle window resize events"""
        # This method is called when the window is resized
        # The layouts will automatically adjust the widgets
        # No need to call super as we're not a true QWidget subclass
        pass

    def load_food_lists(self):
        """Load food lists and their products"""
        if not self.user:
            return

        # Get all food lists
        self.food_lists = self.database.get_all_food_lists()

        # Clear existing tabs
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)

        # Create tabs for each food list
        for i, food_list in enumerate(self.food_lists):
            food_list_id = food_list[0]
            food_list_name = food_list[1]

            # Create a tab for this food list
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"tab_{food_list_id}")

            # Create layout for the tab
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(10, 10, 10, 10)

            # Table widget for this food list's products
            table = QtWidgets.QTableWidget()
            table.setObjectName(f"table_{food_list_id}")
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Product Name", "Perishable", "Quantity"])

            # Set columns to stretch
            header = table.horizontalHeader()
            for col in range(4):
                header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

            # Add table to tab layout
            tab_layout.addWidget(table)

            # Load products for this food list
            self.load_products_for_list(food_list_id, table)

            # Add the tab to the tab widget
            tab_name = f"Food List {food_list_id}"
            self.tab_widget.addTab(tab, tab_name)

    def load_products_for_list(self, food_list_id, table):
        """Load products for a specific food list into the provided table"""
        # Get food list data
        food_list_data = self.database.get_food_list(food_list_id)

        if not food_list_data or 'products' not in food_list_data:
            return

        products = food_list_data['products']

        # Clear the table
        table.setRowCount(0)

        # Populate the table
        for row, product in enumerate(products):
            product_id = product[0]
            product_name = product[1]
            perishable = "Yes" if product[2] else "No"
            quantity = product[3]

            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            table.setItem(row, 1, QTableWidgetItem(product_name))
            table.setItem(row, 2, QTableWidgetItem(perishable))
            table.setItem(row, 3, QTableWidgetItem(str(quantity)))

    def go_back(self):
        """Go back to the main menu"""
        if self.user and self.user[6]:  # User is admin
            self.main_window.show_admin_menu(self.user)
        elif self.user:
            self.main_window.show_user_menu(self.user) 