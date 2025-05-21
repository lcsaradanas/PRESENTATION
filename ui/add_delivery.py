from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QDate, QTime

class AddDeliveryScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None

    def set_user(self, user):
        self.user = user
        self.load_data()

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1301, 811)

        # Main widget with background - fill the entire parent widget
        self.widget = QtWidgets.QWidget(Widget)

        # Use a layout for the parent Widget to ensure the background fills everything
        layout = QVBoxLayout(Widget)
        layout.setContentsMargins(0, 0, 0, 0) # No margins to ensure full coverage
        layout.setSpacing(0)
        layout.addWidget(self.widget)

        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(158, 198, 243);}")
        self.widget.setObjectName("widget")

        # Main layout for the content
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(60, 30, 60, 30)

        # Title area
        self.title_layout = QHBoxLayout()
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Title
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 36pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("ADD DELIVER")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.title_layout.addWidget(self.label)
        self.title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.title_layout)

        # Subtitle
        self.subtitle_layout = QHBoxLayout()
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Schedule a new delivery")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.subtitle_layout.addWidget(self.label_2)
        self.subtitle_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.subtitle_layout)

        # Add vertical space between subtitle and form
        self.main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Form layout
        self.form_layout = QGridLayout()
        self.form_layout.setHorizontalSpacing(10)
        self.form_layout.setVerticalSpacing(20)

        # Date field
        self.label_3 = QtWidgets.QLabel("DATE OF DELIVERY")
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.form_layout.addWidget(self.label_3, 0, 0)

        self.date_field = QtWidgets.QDateEdit()
        self.date_field.setMinimumSize(QtCore.QSize(421, 41))
        self.date_field.setCalendarPopup(True)
        self.date_field.setDate(QDate.currentDate())
        self.form_layout.addWidget(self.date_field, 1, 0)

        # Departure Time field
        self.label_4 = QtWidgets.QLabel("DELIVERY TIME")
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.form_layout.addWidget(self.label_4, 2, 0)

        self.departure_time = QtWidgets.QTimeEdit()
        self.departure_time.setMinimumSize(QtCore.QSize(421, 41))
        self.departure_time.setTime(QTime(9, 0))
        self.form_layout.addWidget(self.departure_time, 3, 0)

        # Food List field
        self.label_6 = QtWidgets.QLabel("FOOD LIST")
        self.label_6.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.form_layout.addWidget(self.label_6, 4, 0)

        self.food_list_combo = QtWidgets.QComboBox()
        self.food_list_combo.setMinimumSize(QtCore.QSize(421, 41))
        self.form_layout.addWidget(self.food_list_combo, 5, 0)

        # Location field
        self.label_7 = QtWidgets.QLabel("LOCATION")
        self.label_7.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.form_layout.addWidget(self.label_7, 6, 0)

        self.location_combo = QtWidgets.QComboBox()
        self.location_combo.setMinimumSize(QtCore.QSize(421, 41))
        self.form_layout.addWidget(self.location_combo, 7, 0)

        # Organization field
        self.label_8 = QtWidgets.QLabel("ORGANIZATION")
        self.label_8.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.form_layout.addWidget(self.label_8, 8, 0)

        self.org_combo = QtWidgets.QComboBox()
        self.org_combo.setMinimumSize(QtCore.QSize(421, 41))
        self.form_layout.addWidget(self.org_combo, 9, 0)

        self.error_label = QtWidgets.QLabel("")
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\"; color:red;")
        self.form_layout.addWidget(self.error_label, 10, 0, 1, 2)

        # Buttons column
        self.button_layout = QVBoxLayout()

        # Add Delivery button
        self.add_button = QtWidgets.QPushButton("ADD DELIVERY")
        self.add_button.setMinimumSize(QtCore.QSize(191, 61))
        self.add_button.setStyleSheet("""
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
        self.button_layout.addWidget(self.add_button)

        # Add spacing between buttons
        self.button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Back button
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setMinimumSize(QtCore.QSize(191, 61))
        self.back_button.setStyleSheet("""
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

        self.button_layout.addWidget(self.back_button)

        # Form and buttons container
        self.form_container = QGridLayout()
        self.form_container.setColumnStretch(0, 1)
        self.form_container.setColumnStretch(1, 0)
        self.form_container.setColumnStretch(2, 1)


        self.form_container.addLayout(self.form_layout, 0, 1, alignment=QtCore.Qt.AlignCenter)
        self.form_container.addLayout(self.button_layout, 1, 2, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.main_layout.addLayout(self.form_container)
        self.main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Connect buttons
        self.add_button.clicked.connect(self.add_delivery)
        self.back_button.clicked.connect(self.go_back)

        # Resize handling
        Widget.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Handle window resize events"""
        # This method is called when the window is resized
        # The layouts will automatically adjust the widgets
        # No need to call super as we're not a true QWidget subclass
        pass

    def load_data(self):
        """Load data for dropdown menus"""
        if not self.user:
            return

        # Clear the combo boxes first
        self.food_list_combo.clear()
        self.location_combo.clear()
        self.org_combo.clear()

        #Load food lists
        food_lists = self.database.get_all_food_lists()
        for food_list in food_lists:
            self.food_list_combo.addItem(food_list[1], food_list[0])

        # Load locations
        locations = self.database.get_all_locations()
        for location in locations:
            self.location_combo.addItem(location[1], location[0])

        #Load organizations
        organizations = self.database.get_all_organizations()
        for org in organizations:
            self.org_combo.addItem(org[1], org[0])

    def add_delivery(self):
        """Add a new delivery to the database"""
        # Get the date and ensure it's in the correct format
        qdate = self.date_field.date()
        date = qdate.toString("yyyy-MM-dd")
        departure_time = self.departure_time.time().toString("hh:mm")
        # We're not using arrival time anymore, pass None/NULL to the database
        arrival_time = None

        # Get IDs from comboboxes
        food_list_id = self.food_list_combo.currentData()
        location_id = self.location_combo.currentData()
        org_id = self.org_combo.currentData()

        # Validate inputs
        if not food_list_id or not location_id or not org_id:
            self.error_label.setText("Please select all required fields")
            return

        # Add delivery to database
        delivery_id, error = self.database.add_delivery(departure_time, arrival_time, date, food_list_id, location_id, org_id)

        if error:
            self.error_label.setText(error)
            return

        # Show success message
        QMessageBox.information(self.widget, "Success", "Delivery scheduled successfully!")

        # Reset all form fields to their default values
        self.reset_form()

    def reset_form(self):
        """Reset all form fields to default values"""
        # Reset date to current date
        self.date_field.setDate(QDate.currentDate())

        # Reset time to default (9:00 AM)
        self.departure_time.setTime(QTime(9, 0))

        # Reset comboboxes to first item if they have items
        if self.food_list_combo.count() > 0:
            self.food_list_combo.setCurrentIndex(0)
        if self.location_combo.count() > 0:
            self.location_combo.setCurrentIndex(0)
        if self.org_combo.count() > 0:
            self.org_combo.setCurrentIndex(0)

        # Clear any error message
        self.error_label.setText("")

    def go_back(self):
        self.main_window.show_admin_menu(self.user)
