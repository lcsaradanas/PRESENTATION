from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
import sqlite3


class ViewDeliveryUserScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None

    def set_user(self, user):
        self.user = user
        self.load_deliveries()

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

        # Main layout for the content
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(60, 40, 60, 40)
        self.main_layout.setSpacing(20)

        # Title area with center alignment
        self.title_layout = QVBoxLayout()
        self.title_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Title
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 36pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("VIEW DELIVERIES")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.label)

        # Subtitle
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Deliveries assigned to your organization")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.label_2)

        # Add title section to main layout
        self.main_layout.addLayout(self.title_layout)

        # Add spacing after title
        self.main_layout.addSpacing(10)

        # Filter and search area
        self.filter_search_layout = QHBoxLayout()
        self.filter_search_layout.setContentsMargins(0, 10, 0, 10)
        self.filter_search_layout.setSpacing(10)

        # Filter section
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("FILTER BY:")
        self.label_3.setMinimumWidth(100)
        self.label_3.setMaximumWidth(100)
        self.filter_search_layout.addWidget(self.label_3)

        # Filter combobox
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.setMinimumWidth(150)
        self.filter_combo.setMaximumWidth(250)
        self.filter_combo.setMinimumHeight(35)
        self.filter_combo.setObjectName("filter_combo")
        self.filter_combo.addItem("All")
        self.filter_combo.addItem("Upcoming")
        self.filter_combo.addItem("Past")
        self.filter_search_layout.addWidget(self.filter_combo)

        # Add spacing between filter and search
        self.filter_search_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # Search section
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("SEARCH:")
        self.label_4.setMinimumWidth(80)
        self.label_4.setMaximumWidth(80)
        self.filter_search_layout.addWidget(self.label_4)

        # Search field
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setMinimumHeight(35)
        self.search_field.setObjectName("search_field")
        self.filter_search_layout.addWidget(self.search_field, 1)  # 1 is stretch factor

        self.main_layout.addLayout(self.filter_search_layout)

        # Table widget for deliveries
        self.delivery_table = QtWidgets.QTableWidget()
        self.delivery_table.setMinimumHeight(400)
        self.delivery_table.setObjectName("delivery_table")
        self.delivery_table.setColumnCount(5)
        self.delivery_table.setHorizontalHeaderLabels(["ID", "Delivery Time", "Date", "Location", "Food List"])

        # Make columns stretch to fill available space
        header = self.delivery_table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.main_layout.addWidget(self.delivery_table, 1)  # 1 is stretch factor

        # Bottom section for back button
        self.bottom_layout = QHBoxLayout()

        # Back button (left-aligned)
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setMinimumSize(QtCore.QSize(161, 41))
        self.back_button.setMaximumSize(QtCore.QSize(161, 41))
        self.back_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: rgb(255, 225, 189);
                font: 75 12pt "Century Gothic";
                border: 2px solid orange;
            }
            QPushButton:hover {
                background-color: rgb(255, 235, 210);
            }
        """)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")
        self.bottom_layout.addWidget(self.back_button)

        # Add spacer to push button to left
        self.bottom_layout.addStretch()

        self.main_layout.addLayout(self.bottom_layout)

        # Connect the buttons to their functions
        self.filter_combo.currentTextChanged.connect(self.load_deliveries)
        self.search_field.textChanged.connect(self.load_deliveries)
        self.back_button.clicked.connect(self.go_back)

        # Set minimum size to ensure all content is visible
        Widget.setMinimumSize(1000, 600)

    def load_deliveries(self):
        """Load deliveries from the database based on the user organization"""
        if not self.user:
            return

        # Get the organization ID for this user
        org_id = None

        try:
            # Get filter values
            filter_by = self.filter_combo.currentText().lower() if self.filter_combo.currentText() != "All" else None
            search_term = self.search_field.text() if self.search_field.text() else None

            # Force database connection refresh before fetching data
            self.database.refresh_connection()

            # First find the organization for this user
            # Using direct query to find the org_id for the current user
            self.database.cursor.execute("""
                                         SELECT o.org_id
                                         FROM org_info o
                                                  JOIN accounts a ON o.user_code = a.user_code
                                         WHERE a.user_code = ?
                                         """, (self.user[0],))

            org_result = self.database.cursor.fetchone()
            if not org_result:
                return  # No organization found for this user

            org_id = org_result[0]

            # Now get the deliveries for this organization
            query = """
                    SELECT d.delivery_id, \
                           d.departure_time, \
                           d.date, \
                           l.location_name AS location, \
                           f.name          AS food_list
                    FROM delivery d
                             JOIN food_list f ON d.foodList_id = f.foodList_id
                             JOIN location_info l ON d.location_id = l.location_id
                    WHERE d.org_id = ? \
                    """

            params = [org_id]

            # Add filter conditions if needed
            if filter_by == "past":
                query += " AND date(d.date) < date('now')"
            elif filter_by == "upcoming":
                query += " AND date(d.date) >= date('now')"

            if search_term:
                query += f""" AND (
                    f.name LIKE '%{search_term}%' OR 
                    l.location_name LIKE '%{search_term}%'
                )"""

            query += " ORDER BY d.date DESC"

            # Execute query
            self.database.cursor.execute(query, params)
            deliveries = self.database.cursor.fetchall()

            # Clear the table
            self.delivery_table.setRowCount(0)

            # Populate the table with exact column mapping
            row = 0
            for delivery in deliveries:
                # Fields now exactly match display order from our query
                delivery_id = delivery[0]
                departure_time = delivery[1] if delivery[1] else "N/A"
                date = delivery[2]
                location = delivery[3]  # Location name is now directly at index 3
                food_list = delivery[4]  # Food list name is now directly at index 4

                # Skip if search term is specified and doesn't match
                if search_term and search_term.lower() not in str(food_list).lower() and search_term.lower() not in str(
                        location).lower():
                    continue

                self.delivery_table.insertRow(row)
                self.delivery_table.setItem(row, 0, QTableWidgetItem(str(delivery_id)))
                self.delivery_table.setItem(row, 1, QTableWidgetItem(str(departure_time)))
                self.delivery_table.setItem(row, 2, QTableWidgetItem(str(date)))
                self.delivery_table.setItem(row, 3, QTableWidgetItem(str(location)))
                self.delivery_table.setItem(row, 4, QTableWidgetItem(str(food_list)))
                row += 1
        except Exception as e:
            print(f"Error loading user deliveries: {e}")

    def go_back(self):
        """Go back to the main menu"""
        self.main_window.show_user_menu(self.user) 