from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from ui.screen_helper import ScreenHelper


class ViewOrganizationScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None

    def set_user(self, user):
        self.user = user
        self.load_organizations()

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1301, 811)

        self.widget = QtWidgets.QWidget(Widget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1301, 811))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(158, 198, 243);}")
        self.widget.setObjectName("widget")

        # Title
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(350, 50, 601, 91))
        self.label.setStyleSheet("font: 34pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("VIEW ORGANIZATIONS")

        # Subtitle
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(430, 130, 451, 41))
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("List of all registered organizations")

        # Search section
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(190, 190, 121, 31))
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("SEARCH:")

        # Search field
        self.search_field = QtWidgets.QLineEdit(self.widget)
        self.search_field.setGeometry(QtCore.QRect(320, 190, 691, 31))
        self.search_field.setObjectName("search_field")

        # Apply filter button
        self.apply_filter = QtWidgets.QPushButton(self.widget)
        self.apply_filter.setGeometry(QtCore.QRect(1030, 190, 161, 31))
        self.apply_filter.setStyleSheet("border-radius: 10px;\n"
                                        "background-color:rgb(187, 216, 163);\n"
                                        "font: 75 12pt \"Century Gothic\";\n"
                                        "border: 2px solid green")
        self.apply_filter.setObjectName("apply_filter")
        self.apply_filter.setText("SEARCH")

        # Table widget for organizations
        self.org_table = QtWidgets.QTableWidget(self.widget)
        self.org_table.setGeometry(QtCore.QRect(190, 250, 921, 451))
        self.org_table.setObjectName("org_table")
        self.org_table.setColumnCount(4)
        self.org_table.setHorizontalHeaderLabels(["ID", "Organization Name", "Location", "Contact Person"])

        # Make columns stretch to fill available space
        header = self.org_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        # Back button
        self.back_button = QtWidgets.QPushButton(self.widget)
        self.back_button.setGeometry(QtCore.QRect(190, 730, 161, 41))
        self.back_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: rgb(255, 225, 189);
                font: 75 12pt "Century Gothic";
                border: 2px solid orange;
            }
            QPushButton:hover {
                background-color: rgb(240, 200, 150);
            }
        """)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")

        # Connect the buttons to their functions
        self.apply_filter.clicked.connect(self.apply_search)
        self.back_button.clicked.connect(self.go_back)

        # Apply initial resizing
        Widget.resizeEvent = self.handle_resize_event

    def handle_resize_event(self, event):
        """Handle resize events for this widget"""
        # Call parent resizeEvent
        QtWidgets.QWidget.resizeEvent(self.widget.parent(), event)

        # Resize main widget to fill the entire parent
        if self.widget.parent():
            parent_width = self.widget.parent().width()
            parent_height = self.widget.parent().height()

            # Resize the main widget to fill the window
            self.widget.setGeometry(0, 0, parent_width, parent_height)

            # Adjust the table size based on the new window size
            table_height = parent_height - 350  # Adjust based on spacing
            if table_height > 200:  # Minimum table height
                self.org_table.setFixedHeight(int(table_height))

            # Adjust table width and position
            table_width = min(parent_width - 200, 1100)  # Reduce maximum width
            table_x = int((parent_width - table_width) / 2)
            self.org_table.setGeometry(QtCore.QRect(table_x, 250, int(table_width), int(table_height)))

            # Center the title labels
            center_x = int(parent_width / 2)
            self.label.setGeometry(QtCore.QRect(int(center_x - 300), 50, 601, 91))
            self.label_2.setGeometry(QtCore.QRect(int(center_x - 225), 130, 451, 41))

            # Position search controls
            search_y = 190
            search_field_width = int(table_width - 300)
            self.label_4.setGeometry(QtCore.QRect(table_x, search_y, 121, 31))
            self.search_field.setGeometry(QtCore.QRect(table_x + 130, search_y, search_field_width, 31))

            # Position search button directly after search field
            search_button_x = table_x + 130 + search_field_width + 10  # 10px gap
            self.apply_filter.setGeometry(QtCore.QRect(search_button_x, search_y, 161, 31))

            # Position back button - fixed distance from left edge and bottom
            back_button_margin = 50
            back_button_y = int(table_height + 280)  # Position below table with padding

            # Ensure back button is visible even on smaller screens
            if back_button_y > parent_height - 80:
                back_button_y = parent_height - 80

            self.back_button.setGeometry(QtCore.QRect(table_x, back_button_y, 161, 41))

    def load_organizations(self):
        """Load organizations from database into the table"""
        if not self.user:
            return

        # Get search term
        search_term = self.search_field.text() if self.search_field.text() else None

        # Get organizations
        organizations = self.database.get_all_organizations(search_term)

        # Clear the table
        self.org_table.setRowCount(0)

        # Populate the table
        row = 0
        for org in organizations:
            org_id = org[0]
            org_name = org[1]
            location = org[2]
            contact_person = org[3]

            self.org_table.insertRow(row)
            self.org_table.setItem(row, 0, QTableWidgetItem(str(org_id)))
            self.org_table.setItem(row, 1, QTableWidgetItem(org_name))
            self.org_table.setItem(row, 2, QTableWidgetItem(location))
            self.org_table.setItem(row, 3, QTableWidgetItem(contact_person))
            row += 1

    def apply_search(self):
        """Apply search filter to organizations table"""
        self.load_organizations()

    def go_back(self):
        """Go back to the main menu"""
        self.main_window.show_admin_menu(self.user) 