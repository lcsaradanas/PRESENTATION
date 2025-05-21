from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, QTime
import sqlite3


class EditDeliveryScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.selected_delivery_id = None

    def set_user(self, user):
        self.user = user
        self.load_deliveries()
        self.load_data()

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
        self.label.setGeometry(QtCore.QRect(430, 20, 441, 61))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font: 36pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("EDIT DELIVERY")

        # Subtitle
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(430, 80, 451, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Select a delivery to edit")

        # Filter section
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(190, 120, 121, 31))
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("FILTER BY:")

        # Filter combobox
        self.filter_combo = QtWidgets.QComboBox(self.widget)
        self.filter_combo.setGeometry(QtCore.QRect(320, 120, 251, 31))
        self.filter_combo.setObjectName("filter_combo")
        self.filter_combo.addItem("All")
        self.filter_combo.addItem("Upcoming")
        self.filter_combo.addItem("Past")

        # Search section
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(610, 120, 121, 31))
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("SEARCH:")

        # Search field
        self.search_field = QtWidgets.QLineEdit(self.widget)
        self.search_field.setGeometry(QtCore.QRect(730, 120, 381, 31))
        self.search_field.setObjectName("search_field")

        # Table widget for deliveries
        self.delivery_table = QtWidgets.QTableWidget(self.widget)
        self.delivery_table.setGeometry(
            QtCore.QRect(190, 160, 921, 260))  # Adjust height since we removed the filter button
        self.delivery_table.setObjectName("delivery_table")
        self.delivery_table.setColumnCount(6)
        self.delivery_table.setHorizontalHeaderLabels(
            ["ID", "Delivery Time", "Date", "Organization", "Location", "Food List"])

        # Make columns stretch to fill available space
        header = self.delivery_table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        # Edit section
        self.edit_section = QtWidgets.QGroupBox(self.widget)
        self.edit_section.setGeometry(QtCore.QRect(190, 430, 921, 340))
        self.edit_section.setStyleSheet("QGroupBox{\n"
                                        "background-color: rgb(200, 220, 240);\n"
                                        "border: 2px solid rgb(76, 107, 140);\n"
                                        "border-radius: 10px;\n"
                                        "padding: 10px;\n"
                                        "}\n")
        self.edit_section.setTitle("")
        self.edit_section.setObjectName("edit_section")

        # Selected delivery label
        self.selected_label = QtWidgets.QLabel(self.edit_section)
        self.selected_label.setGeometry(QtCore.QRect(20, 20, 201, 31))
        self.selected_label.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.selected_label.setObjectName("selected_label")
        self.selected_label.setText("SELECTED DELIVERY:")

        self.selected_delivery_label = QtWidgets.QLabel(self.edit_section)
        self.selected_delivery_label.setGeometry(QtCore.QRect(230, 20, 671, 31))
        self.selected_delivery_label.setStyleSheet("font: 12pt \"Century Gothic\"; color: rgb(76, 107, 140)")
        self.selected_delivery_label.setObjectName("selected_delivery_label")
        self.selected_delivery_label.setText("None")

        # Date field
        self.label_5 = QtWidgets.QLabel(self.edit_section)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 121, 21))
        self.label_5.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_5.setObjectName("label_5")
        self.label_5.setText("DATE")

        self.date_field = QtWidgets.QDateEdit(self.edit_section)
        self.date_field.setGeometry(QtCore.QRect(20, 100, 201, 41))
        self.date_field.setCalendarPopup(True)
        self.date_field.setDate(QDate.currentDate())
        self.date_field.setObjectName("date_field")

        # Departure Time field
        self.label_6 = QtWidgets.QLabel(self.edit_section)
        self.label_6.setGeometry(QtCore.QRect(250, 70, 181, 21))
        self.label_6.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_6.setObjectName("label_6")
        self.label_6.setText("DELIVERY TIME")

        self.departure_time = QtWidgets.QTimeEdit(self.edit_section)
        self.departure_time.setGeometry(QtCore.QRect(250, 100, 201, 41))
        self.departure_time.setTime(QTime(9, 0))  # Default 9:00 AM
        self.departure_time.setObjectName("departure_time")

        # Food List field
        self.label_8 = QtWidgets.QLabel(self.edit_section)
        self.label_8.setGeometry(QtCore.QRect(20, 160, 151, 21))
        self.label_8.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_8.setObjectName("label_8")
        self.label_8.setText("FOOD LIST")

        self.food_list_combo = QtWidgets.QComboBox(self.edit_section)
        self.food_list_combo.setGeometry(QtCore.QRect(20, 190, 201, 41))
        self.food_list_combo.setObjectName("food_list_combo")

        # Location field
        self.label_9 = QtWidgets.QLabel(self.edit_section)
        self.label_9.setGeometry(QtCore.QRect(250, 160, 151, 21))
        self.label_9.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_9.setObjectName("label_9")
        self.label_9.setText("LOCATION")

        self.location_combo = QtWidgets.QComboBox(self.edit_section)
        self.location_combo.setGeometry(QtCore.QRect(250, 190, 201, 41))
        self.location_combo.setObjectName("location_combo")

        # Organization field
        self.label_10 = QtWidgets.QLabel(self.edit_section)
        self.label_10.setGeometry(QtCore.QRect(480, 160, 151, 21))
        self.label_10.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_10.setObjectName("label_10")
        self.label_10.setText("ORGANIZATION")

        self.org_combo = QtWidgets.QComboBox(self.edit_section)
        self.org_combo.setGeometry(QtCore.QRect(480, 190, 201, 41))
        self.org_combo.setObjectName("org_combo")

        # Update button
        self.update_button = QtWidgets.QPushButton(self.edit_section)
        self.update_button.setGeometry(QtCore.QRect(480, 250, 191, 61))
        self.update_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #BBD8A3;
                color: black;
                font: 75 18pt "Century Gothic";
                border: 2px solid green;
            }
            QPushButton:hover {
                background-color: #A6C18F;
            }
        """)
        self.update_button.setObjectName("update_button")
        self.update_button.setText("UPDATE")

        # Back button
        self.back_button = QtWidgets.QPushButton(self.widget)
        self.back_button.setGeometry(QtCore.QRect(190, 780, 161, 31))
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

        # Error message label
        self.error_label = QtWidgets.QLabel(self.edit_section)
        self.error_label.setGeometry(QtCore.QRect(20, 250, 441, 31))
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")

        # Connect the buttons to their functions
        self.filter_combo.currentTextChanged.connect(self.load_deliveries)
        self.search_field.textChanged.connect(self.load_deliveries)
        self.back_button.clicked.connect(self.go_back)
        self.update_button.clicked.connect(self.update_delivery)
        self.delivery_table.itemSelectionChanged.connect(self.on_selection_change)

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

            # Center the title labels
            center_x = int(parent_width / 2)
            self.label.setGeometry(QtCore.QRect(int(center_x - 220), 20, 441, 61))
            self.label_2.setGeometry(QtCore.QRect(int(center_x - 225), 80, 451, 31))

            # Calculate margins and content width
            margin_x = int(max(50, (parent_width - 1100) / 2))  # Min 50px, max 1100px width
            content_width = min(parent_width - 2 * margin_x, 1100)

            # Position filter controls
            self.label_3.setGeometry(QtCore.QRect(margin_x, 120, 121, 31))
            self.filter_combo.setGeometry(QtCore.QRect(margin_x + 130, 120, 251, 31))

            # Position search controls
            search_label_x = margin_x + 400
            self.label_4.setGeometry(QtCore.QRect(search_label_x, 120, 121, 31))

            # Calculate search field width based on available space
            search_field_width = content_width - 500  # Allow space for labels and margins
            self.search_field.setGeometry(QtCore.QRect(search_label_x + 120, 120, search_field_width, 31))

            # Adjust table position and size
            table_y = 160
            self.delivery_table.setGeometry(QtCore.QRect(margin_x, table_y, content_width, 260))

            # Position edit section below table with spacing
            edit_section_y = 210 + table_y
            self.edit_section.setGeometry(QtCore.QRect(margin_x, edit_section_y, content_width, 340))

            # Position back button at bottom
            back_button_y = edit_section_y + 340 + 20

            # Make sure back button stays visible
            if back_button_y > parent_height - 50:
                back_button_y = parent_height - 50

            self.back_button.setGeometry(QtCore.QRect(margin_x, back_button_y, 161, 31))

    def load_data(self):
        """Load data for dropdown menus"""
        # Clear the comboboxes first
        self.food_list_combo.clear()
        self.location_combo.clear()
        self.org_combo.clear()

        # Load food lists
        food_lists = self.database.get_all_food_lists()
        for food_list in food_lists:
            self.food_list_combo.addItem(food_list[1], food_list[0])

        # Load locations
        locations = self.database.get_all_locations()
        for location in locations:
            self.location_combo.addItem(location[1], location[0])

        # Load organizations
        organizations = self.database.get_all_organizations()
        for org in organizations:
            self.org_combo.addItem(org[1], org[0])

    def load_deliveries(self):
        """Load deliveries from the database"""
        if not self.user:
            return

        # Get filter values
        filter_by = self.filter_combo.currentText().lower() if self.filter_combo.currentText() != "All" else None
        search_term = self.search_field.text() if self.search_field.text() else None

        try:
            # Connect directly to the database to control exactly what data we get
            conn = sqlite3.connect("donationdriveDBMS.db")
            cursor = conn.cursor()

            # Use a direct query that explicitly gets fields in the order we want to display them
            query = """
                    SELECT d.delivery_id, \
                           d.departure_time, \
                           d.date, \
                           o.name          AS organization, \
                           l.location_name AS location, \
                           f.name          AS food_list
                    FROM delivery d
                             JOIN food_list f ON d.foodList_id = f.foodList_id
                             JOIN org_info o ON d.org_id = o.org_id
                             JOIN location_info l ON d.location_id = l.location_id \
                    """

            # Add filter conditions if needed
            where_clauses = []
            if filter_by == "past":
                where_clauses.append("date(d.date) < date('now')")
            elif filter_by == "upcoming":
                where_clauses.append("date(d.date) >= date('now')")

            if search_term:
                where_clauses.append(f"""(
                    f.name LIKE '%{search_term}%' OR 
                    o.name LIKE '%{search_term}%' OR 
                    l.location_name LIKE '%{search_term}%'
                )""")

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            query += " ORDER BY d.date DESC"

            # Execute query
            cursor.execute(query)
            deliveries = cursor.fetchall()

            # Clear the table
            self.delivery_table.setRowCount(0)

            # Populate the table with exact column mapping
            row = 0
            for delivery in deliveries:
                # Fields now exactly match display order from our query
                delivery_id = delivery[0]
                departure_time = delivery[1] if delivery[1] else "N/A"
                date = delivery[2]
                organization = delivery[3]  # Organization name is now directly at index 3
                location = delivery[4]  # Location name is now directly at index 4
                food_list = delivery[5]  # Food list name is now directly at index 5

                self.delivery_table.insertRow(row)
                self.delivery_table.setItem(row, 0, QTableWidgetItem(str(delivery_id)))
                self.delivery_table.setItem(row, 1, QTableWidgetItem(str(departure_time)))
                self.delivery_table.setItem(row, 2, QTableWidgetItem(str(date)))
                self.delivery_table.setItem(row, 3, QTableWidgetItem(str(organization)))
                self.delivery_table.setItem(row, 4, QTableWidgetItem(str(location)))
                self.delivery_table.setItem(row, 5, QTableWidgetItem(str(food_list)))
                row += 1

            conn.close()
        except Exception as e:
            print(f"Error loading deliveries: {e}")

    def on_selection_change(self):
        """Handle selection changes in the table"""
        selected_rows = self.delivery_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            delivery_id = self.delivery_table.item(row, 0).text()
            departure_time = self.delivery_table.item(row, 1).text()
            date = self.delivery_table.item(row, 2).text()  # This is now the correct date from the table
            location = self.delivery_table.item(row, 4).text()
            organization = self.delivery_table.item(row, 3).text()
            food_list = self.delivery_table.item(row, 5).text()

            self.selected_delivery_id = delivery_id
            self.selected_delivery_label.setText(f"ID: {delivery_id} - {date} at {location}")

            # Set form values
            # Parse date (assuming format YYYY-MM-DD)
            try:
                year, month, day = map(int, date.split('-'))
                self.date_field.setDate(QDate(year, month, day))
            except:
                self.date_field.setDate(QDate.currentDate())

            # Parse times (assuming format HH:MM)
            try:
                if departure_time != "N/A":
                    hour, minute = map(int, departure_time.split(':'))
                    self.departure_time.setTime(QTime(hour, minute))
            except:
                self.departure_time.setTime(QTime(9, 0))

            # Set comboboxes
            # Find and select the right indices
            self.select_combobox_item(self.location_combo, location)
            self.select_combobox_item(self.org_combo, organization)
            self.select_combobox_item(self.food_list_combo, food_list)
        else:
            self.selected_delivery_id = None
            self.selected_delivery_label.setText("None")
            self.date_field.setDate(QDate.currentDate())
            self.departure_time.setTime(QTime(9, 0))

    def select_combobox_item(self, combobox, text):
        """Select an item in a combobox by its text"""
        index = combobox.findText(text)
        if index >= 0:
            combobox.setCurrentIndex(index)

    def update_delivery(self):
        """Update the selected delivery information"""
        if not self.selected_delivery_id:
            QMessageBox.warning(self.widget, "Warning", "Please select a delivery to update")
            return

        date = self.date_field.date().toString("yyyy-MM-dd")
        departure_time = self.departure_time.time().toString("hh:mm")

        # Get IDs from comboboxes
        food_list_id = self.food_list_combo.currentData()
        location_id = self.location_combo.currentData()
        org_id = self.org_combo.currentData()

        # Validate inputs
        if not food_list_id or not location_id or not org_id:
            self.error_label.setText("Please select all required fields")
            return

        # Update delivery in database
        success, error = self.database.update_delivery(
            self.selected_delivery_id,
            departure_time,
            date,
            food_list_id,
            location_id,
            org_id
        )

        if success:
            QMessageBox.information(self.widget, "Success", "Delivery updated successfully!")
            self.error_label.setText("")
            self.load_deliveries()
        else:
            self.error_label.setText(f"Failed to update delivery: {error}")

    def go_back(self):
        """Go back to the admin menu"""
        self.selected_delivery_id = None
        self.main_window.show_admin_menu(self.user) 