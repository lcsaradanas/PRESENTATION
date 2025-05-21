from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class CreateAccountScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.validators = {
            'username': False,
            'firstname': False,
            'lastname': False,
            'password': False,
            'confirmpassword': False,
            'organization': True  # Default to true as it's only required for users
        }

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1301, 811)
        self.widget = QtWidgets.QWidget(Widget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1301, 811))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(158, 198, 243);}")
        self.widget.setObjectName("widget")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(320, 60, 741, 171))
        self.label.setStyleSheet("font: 48pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(500, 170, 451, 61))
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")

        # User Type radio buttons - moved to the top to control organization visibility
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(430, 240, 151, 16))
        self.label_8.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_8.setObjectName("label_8")

        self.user_type_group = QtWidgets.QButtonGroup(Widget)

        self.admin_radio = QtWidgets.QRadioButton(self.widget)
        self.admin_radio.setGeometry(QtCore.QRect(430, 270, 100, 30))
        self.admin_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.admin_radio.setObjectName("admin_radio")

        self.user_radio = QtWidgets.QRadioButton(self.widget)
        self.user_radio.setGeometry(QtCore.QRect(550, 270, 100, 30))
        self.user_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.user_radio.setObjectName("user_radio")
        self.user_radio.setChecked(True)  # Default selection

        self.user_type_group.addButton(self.admin_radio)
        self.user_type_group.addButton(self.user_radio)

        # Organization field
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(430, 310, 151, 16))
        self.label_9.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_9.setObjectName("label_9")

        self.organization = QtWidgets.QLineEdit(self.widget)
        self.organization.setGeometry(QtCore.QRect(430, 330, 421, 41))
        self.organization.setObjectName("organization")

        # Location field
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setGeometry(QtCore.QRect(430, 380, 151, 16))
        self.label_10.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_10.setObjectName("label_10")

        self.location_combo = QtWidgets.QComboBox(self.widget)
        self.location_combo.setGeometry(QtCore.QRect(430, 400, 421, 41))
        self.location_combo.setObjectName("location_combo")

        # Username field
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(430, 450, 121, 16))
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")

        self.username = QtWidgets.QLineEdit(self.widget)
        self.username.setGeometry(QtCore.QRect(430, 470, 421, 41))
        self.username.setObjectName("username")

        # First Name field
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(430, 520, 151, 16))
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")

        self.firstname = QtWidgets.QLineEdit(self.widget)
        self.firstname.setGeometry(QtCore.QRect(430, 540, 421, 41))
        self.firstname.setObjectName("firstname")

        # Last Name field
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(430, 590, 151, 16))
        self.label_5.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_5.setObjectName("label_5")

        self.lastname = QtWidgets.QLineEdit(self.widget)
        self.lastname.setGeometry(QtCore.QRect(430, 610, 421, 41))
        self.lastname.setObjectName("lastname")

        # Password field
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(430, 660, 151, 16))
        self.label_6.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_6.setObjectName("label_6")

        self.password = QtWidgets.QLineEdit(self.widget)
        self.password.setGeometry(QtCore.QRect(430, 680, 421, 41))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")

        # Confirm Password field
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(430, 730, 200, 16))
        self.label_7.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_7.setObjectName("label_7")

        self.confirmpassword = QtWidgets.QLineEdit(self.widget)
        self.confirmpassword.setGeometry(QtCore.QRect(430, 750, 421, 41))
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setObjectName("confirmpassword")

        # Create Account button
        self.create_button = QtWidgets.QPushButton(self.widget)
        self.create_button.setGeometry(QtCore.QRect(440, 800, 391, 61))
        self.create_button.setStyleSheet("border-radius: 20px;\n"
                                         "background-color:rgb(187, 216, 163);\n"
                                         "font: 75 18pt \"Century Gothic\";\n"
                                         "border: 2px solid green")
        self.create_button.setObjectName("create_button")

        # Back button
        self.back_button = QtWidgets.QPushButton(self.widget)
        self.back_button.setGeometry(QtCore.QRect(190, 750, 161, 41))
        self.back_button.setStyleSheet("border-radius: 10px;\n"
                                       "background-color:rgb(255, 225, 189);\n"
                                       "font: 75 12pt \"Century Gothic\";\n"
                                       "border: 2px solid orange")
        self.back_button.setObjectName("back_button")

        # Error message label
        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setGeometry(QtCore.QRect(430, 870, 421, 31))
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        # Connect the create button to create account function
        self.create_button.clicked.connect(self.create_account)
        self.back_button.clicked.connect(self.go_back)

        # Connect radio buttons to toggle organization visibility
        self.admin_radio.toggled.connect(self.toggle_organization_visibility)
        self.user_radio.toggled.connect(self.toggle_organization_visibility)

        # Connect text change signals for real-time validation
        self.username.textChanged.connect(lambda: self.validate_field('username'))
        self.firstname.textChanged.connect(lambda: self.validate_field('firstname'))
        self.lastname.textChanged.connect(lambda: self.validate_field('lastname'))
        self.password.textChanged.connect(lambda: self.validate_field('password'))
        self.confirmpassword.textChanged.connect(lambda: self.validate_field('confirmpassword'))
        self.organization.textChanged.connect(lambda: self.validate_field('organization'))

        # Load all locations from the database
        self.locations = self.database.get_all_locations()

        # Populate location dropdown
        for location in self.locations:
            self.location_combo.addItem(location[1], location[0])

        # Apply initial visibility based on default radio selection
        self.toggle_organization_visibility()

        # Apply initial resizing
        Widget.resizeEvent = self.handle_resize_event

    def toggle_organization_visibility(self):
        """Toggle the visibility of the organization field based on user type selection"""
        is_admin = self.admin_radio.isChecked()
        self.label_9.setVisible(not is_admin)
        self.organization.setVisible(not is_admin)
        self.label_10.setVisible(not is_admin)
        self.location_combo.setVisible(not is_admin)

        # When admin is selected, clear the organization field
        if is_admin:
            self.organization.clear()

        # Update validators
        self.validators['organization'] = True if is_admin else bool(self.organization.text())
        self.update_create_button_state()

        # Adjust positions of all elements below organization field
        if self.widget.parent():
            # Get the form position from the resize handler
            parent_width = self.widget.parent().width()
            form_width = 421
            form_x = int(parent_width / 2 - form_width / 2)

            # Amount to shift elements (organization field height + spacing + location field height + spacing)
            shift = 140 if is_admin else 0

            # Username field
            username_y_label = 450 - shift if is_admin else 450
            username_y_field = 470 - shift if is_admin else 470
            self.label_3.setGeometry(QtCore.QRect(form_x, username_y_label, 121, 16))
            self.username.setGeometry(QtCore.QRect(form_x, username_y_field, form_width, 41))

            # First Name field
            firstname_y_label = 520 - shift if is_admin else 520
            firstname_y_field = 540 - shift if is_admin else 540
            self.label_4.setGeometry(QtCore.QRect(form_x, firstname_y_label, 151, 16))
            self.firstname.setGeometry(QtCore.QRect(form_x, firstname_y_field, form_width, 41))

            # Last Name field
            lastname_y_label = 590 - shift if is_admin else 590
            lastname_y_field = 610 - shift if is_admin else 610
            self.label_5.setGeometry(QtCore.QRect(form_x, lastname_y_label, 151, 16))
            self.lastname.setGeometry(QtCore.QRect(form_x, lastname_y_field, form_width, 41))

            # Password field
            password_y_label = 660 - shift if is_admin else 660
            password_y_field = 680 - shift if is_admin else 680
            self.label_6.setGeometry(QtCore.QRect(form_x, password_y_label, 151, 16))
            self.password.setGeometry(QtCore.QRect(form_x, password_y_field, form_width, 41))

            # Confirm Password field
            confirm_y_label = 730 - shift if is_admin else 730
            confirm_y_field = 750 - shift if is_admin else 750
            self.label_7.setGeometry(QtCore.QRect(form_x, confirm_y_label, 200, 16))
            self.confirmpassword.setGeometry(QtCore.QRect(form_x, confirm_y_field, form_width, 41))

            # Create Account button
            button_width = 391
            center_x = int(parent_width / 2)
            create_y = 800 - shift if is_admin else 800
            self.create_button.setGeometry(QtCore.QRect(int(center_x - button_width / 2), create_y, button_width, 61))

            # Error message label
            error_y = 870 - shift if is_admin else 870
            self.error_label.setGeometry(QtCore.QRect(int(center_x - form_width / 2), error_y, form_width, 31))

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
            self.label.setGeometry(QtCore.QRect(int(center_x - 370), 60, 741, 171))
            self.label_2.setGeometry(QtCore.QRect(int(center_x - 225), 170, 451, 61))

            # Form width remains fixed, but centered
            form_width = 421
            form_x = int(center_x - form_width / 2)

            # User Type radio buttons (first)
            self.label_8.setGeometry(QtCore.QRect(form_x, 240, 151, 16))
            self.admin_radio.setGeometry(QtCore.QRect(form_x, 270, 100, 30))
            self.user_radio.setGeometry(QtCore.QRect(form_x + 120, 270, 100, 30))

            # Organization field
            self.label_9.setGeometry(QtCore.QRect(form_x, 310, 151, 16))
            self.organization.setGeometry(QtCore.QRect(form_x, 330, form_width, 41))

            # Location field
            self.label_10.setGeometry(QtCore.QRect(form_x, 380, 151, 16))
            self.location_combo.setGeometry(QtCore.QRect(form_x, 400, form_width, 41))

            # Username field
            self.label_3.setGeometry(QtCore.QRect(form_x, 450, 121, 16))
            self.username.setGeometry(QtCore.QRect(form_x, 470, form_width, 41))

            # First Name field
            self.label_4.setGeometry(QtCore.QRect(form_x, 520, 151, 16))
            self.firstname.setGeometry(QtCore.QRect(form_x, 540, form_width, 41))

            # Last Name field
            self.label_5.setGeometry(QtCore.QRect(form_x, 590, 151, 16))
            self.lastname.setGeometry(QtCore.QRect(form_x, 610, form_width, 41))

            # Password field
            self.label_6.setGeometry(QtCore.QRect(form_x, 660, 151, 16))
            self.password.setGeometry(QtCore.QRect(form_x, 680, form_width, 41))

            # Confirm Password field
            self.label_7.setGeometry(QtCore.QRect(form_x, 730, 200, 16))
            self.confirmpassword.setGeometry(QtCore.QRect(form_x, 750, form_width, 41))

            # Create Account button
            button_width = 391
            self.create_button.setGeometry(QtCore.QRect(int(center_x - button_width / 2), 800, button_width, 61))

            # Calculate margin for left side
            margin_x = max(50, int((parent_width - 1100) / 2))

            # Back button - keep it on the left side with proper margin
            back_button_y = parent_height - 80  # Fixed distance from bottom
            self.back_button.setGeometry(QtCore.QRect(margin_x, back_button_y, 161, 41))

            # Error message label - center under create button
            self.error_label.setGeometry(QtCore.QRect(int(center_x - form_width / 2), 870, form_width, 31))

            # Apply organization visibility effects to adjust spacing
            self.toggle_organization_visibility()

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Create Account"))
        self.label.setText(_translate("Widget", "CREATE ACCOUNT"))
        self.label_2.setText(_translate("Widget", "Please fill in the details"))
        self.label_8.setText(_translate("Widget", "USER TYPE"))
        self.admin_radio.setText(_translate("Widget", "Admin"))
        self.user_radio.setText(_translate("Widget", "User"))
        self.label_9.setText(_translate("Widget", "ORGANIZATION"))
        self.label_10.setText(_translate("Widget", "LOCATION"))
        self.label_3.setText(_translate("Widget", "USERNAME"))
        self.label_4.setText(_translate("Widget", "FIRST NAME"))
        self.label_5.setText(_translate("Widget", "LAST NAME"))
        self.label_6.setText(_translate("Widget", "PASSWORD"))
        self.label_7.setText(_translate("Widget", "CONFIRM PASSWORD"))
        self.create_button.setText(_translate("Widget", "CREATE ACCOUNT"))
        self.back_button.setText(_translate("Widget", "BACK"))

    def go_back(self):
        # Go back to welcome screen
        self.main_window.show_welcome_screen()

    def create_account(self):
        # Show loading indicator
        self.error_label.setText("Creating account...")
        QtWidgets.QApplication.processEvents()

        username = self.username.text().strip()
        firstname = self.firstname.text().strip()
        lastname = self.lastname.text().strip()
        password = self.password.text()
        confirm_password = self.confirmpassword.text()
        organization = self.organization.text().strip()

        # Get selected location ID from combo box
        location_id = None
        if self.location_combo.currentIndex() >= 0:
            location_id = self.location_combo.currentData()

        # Check if admin radio button is selected
        user_type = 1 if self.admin_radio.isChecked() else 0

        # Re-validate all inputs as a final check
        if not username or not firstname or not lastname or not password or not confirm_password:
            self.error_label.setText("Please fill in all required fields")
            return

        if len(username) < 3:
            self.error_label.setText("Username must be at least 3 characters")
            return

        if len(password) < 6:
            self.error_label.setText("Password must be at least 6 characters")
            return

        if password != confirm_password:
            self.error_label.setText("Passwords do not match")
            return

        # Regular users should have an organization and location
        if user_type == 0:
            if not organization:
                self.error_label.setText("Please enter an organization for the user")
                return

            if location_id is None:
                self.error_label.setText("Please select a location for the organization")
                return

        # Create account in database
        user_code, error = self.database.create_account(username, firstname, lastname, password, confirm_password,
                                                        user_type)

        if error:
            self.error_label.setText(error)
            return

        # If user is not admin and organization is provided, create the organization
        if user_type == 0 and organization:
            # Add organization
            org_id, org_error = self.database.add_organization(organization, user_code, location_id)

            if org_error:
                self.error_label.setText(f"Account created but could not add organization: {org_error}")
                return

        # Show success message with more details
        success_msg = QMessageBox(self.widget)
        success_msg.setIcon(QMessageBox.Information)
        success_msg.setWindowTitle("Account Created")
        success_msg.setText("Account created successfully!")

        # Add more details to the message
        details = f"Username: {username}\nUser Type: {'Admin' if user_type == 1 else 'User'}"
        if user_type == 0:
            details += f"\nOrganization: {organization}"
        success_msg.setDetailedText(details)

        # Apply styling to make it look better
        success_msg.setStyleSheet("""
            QMessageBox {
                background-color: #f0f8ff;
            }
            QLabel {
                color: #006400;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4682b4;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
        """)

        success_msg.exec_()

        # Reset validation and form state
        for field in self.validators:
            self.validators[field] = field == 'organization'

        # Clear the form
        self.organization.clear()
        self.username.clear()
        self.firstname.clear()
        self.lastname.clear()
        self.password.clear()
        self.confirmpassword.clear()

        # Reset styles
        for field in [self.username, self.firstname, self.lastname, self.password, self.confirmpassword,
                      self.organization]:
            field.setStyleSheet("")

        self.user_radio.setChecked(True)
        self.error_label.setText("")

        # Update button state
        self.update_create_button_state()

        # Go back to login screen
        self.main_window.show_login_screen()

    def validate_field(self, field_name):
        """Validate a specific field and update its visual state"""
        valid = False

        if field_name == 'username':
            text = self.username.text()
            if len(text) >= 3:
                # Check if username already exists
                if self.database.get_user_by_username(text):
                    self.username.setStyleSheet("border: 2px solid red; background-color: #ffeeee;")
                    self.error_label.setText("Username already exists")
                else:
                    valid = True
                    self.username.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                    self.error_label.setText("")
            else:
                self.username.setStyleSheet("border: 1px solid orange;")
                if text:
                    self.error_label.setText("Username must be at least 3 characters")

        elif field_name == 'firstname':
            text = self.firstname.text()
            if text:
                valid = True
                self.firstname.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
            else:
                self.firstname.setStyleSheet("border: 1px solid orange;")

        elif field_name == 'lastname':
            text = self.lastname.text()
            if text:
                valid = True
                self.lastname.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
            else:
                self.lastname.setStyleSheet("border: 1px solid orange;")

        elif field_name == 'password':
            text = self.password.text()
            if len(text) >= 6:
                # Check password strength
                has_upper = any(c.isupper() for c in text)
                has_lower = any(c.islower() for c in text)
                has_digit = any(c.isdigit() for c in text)

                if has_upper and has_lower and has_digit:
                    valid = True
                    self.password.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                    self.error_label.setText("")
                else:
                    self.password.setStyleSheet("border: 2px solid orange; background-color: #ffffee;")
                    self.error_label.setText("Password should have upper, lower case letters and digits")
            else:
                self.password.setStyleSheet("border: 1px solid orange;")
                if text:
                    self.error_label.setText("Password must be at least 6 characters")

            # Also validate confirm password if it has content
            if self.confirmpassword.text():
                self.validate_field('confirmpassword')

        elif field_name == 'confirmpassword':
            text = self.confirmpassword.text()
            if text == self.password.text() and text:
                valid = True
                self.confirmpassword.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                self.error_label.setText("")
            else:
                self.confirmpassword.setStyleSheet("border: 2px solid red; background-color: #ffeeee;")
                if text:
                    self.error_label.setText("Passwords do not match")

        elif field_name == 'organization':
            if self.user_radio.isChecked():  # Only validate if user type is selected
                text = self.organization.text()
                if text:
                    valid = True
                    self.organization.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                else:
                    self.organization.setStyleSheet("border: 1px solid orange;")
            else:
                valid = True  # For admins, org field is not required

        # Update validator state
        self.validators[field_name] = valid

        # Update create button state
        self.update_create_button_state()

    def update_create_button_state(self):
        """Enable or disable create button based on validation state"""
        # Always enable the create button
        self.create_button.setEnabled(True)
        self.create_button.setStyleSheet("""
            border-radius: 20px;
            background-color: rgb(187, 216, 163);
            font: 75 18pt "Century Gothic";
            border: 2px solid green;
        """) 