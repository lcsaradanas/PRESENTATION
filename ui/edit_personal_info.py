from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout


class EditPersonalInfoScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.organization = None
        self.validators = {
            'username': True,  # Initially assume valid since loaded from DB
            'firstname': True,
            'lastname': True,
            'password': True,
            'confirmpassword': True,
            'organization': True
        }
        self.fields_changed = False

    def set_user(self, user):
        print(f"EditPersonalInfo - set_user called with user: {user}")
        self.user = user
        # Set fields_changed to True to enable the update button initially
        self.fields_changed = True
        # Get the user's organization
        if not user[6]:  # If not admin
            print(f"Getting organization for user {user[0]}")
            self.organization = self.database.get_user_organization(user[0])
            print(f"Organization data: {self.organization}")

            # If organization is None, try to find it with a direct database query
            if self.organization is None:
                try:
                    print("Trying direct database query...")
                    self.database.cursor.execute("""
                                                 SELECT o.org_id, o.name, l.location_id, l.location_name
                                                 FROM org_info o
                                                          JOIN location_info l ON o.location_id = l.location_id
                                                 WHERE o.user_code = ?
                                                 """, (user[0],))
                    self.organization = self.database.cursor.fetchone()
                    print(f"Direct query result: {self.organization}")

                    # If still None, create a default organization for this user
                    if self.organization is None:
                        print("Creating default organization for user")
                        org_id, _ = self.database.add_organization(
                            name="CARE Philippines",
                            user_code=user[0],
                            location_id="QC"
                        )
                        if org_id:
                            self.organization = self.database.get_user_organization(user[0])
                            print(f"Created default organization: {self.organization}")
                except Exception as e:
                    print(f"Error with direct query: {str(e)}")
                    # Create a default organization structure to prevent None errors
                    self.organization = (1, "CARE Philippines", "QC", "Quezon City")
        self.load_user_data()

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

        # Main layout for the widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(60, 40, 60, 40)
        self.main_layout.setSpacing(20)

        # Title area
        self.title_layout = QVBoxLayout()
        self.title_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Title
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("font: 36pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("EDIT PERSONAL INFORMATION")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.label)

        # Subtitle
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Update your account information")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.label_2)

        # Add title section to main layout
        self.main_layout.addLayout(self.title_layout)

        # Form layout - this centers the form horizontally
        self.form_container = QHBoxLayout()
        self.form_container.addStretch()

        # Change to QFormLayout instead of QVBoxLayout for better label-field alignment
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Organization field (first field, only visible for regular users)
        self.label_8 = QtWidgets.QLabel()
        self.label_8.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_8.setObjectName("label_8")
        self.label_8.setText("Organization")

        self.organization_field = QtWidgets.QLineEdit()
        self.organization_field.setMinimumSize(QtCore.QSize(400, 41))
        self.organization_field.setMaximumSize(QtCore.QSize(500, 41))
        self.organization_field.setObjectName("organization_field")
        self.form_layout.addRow(self.label_8, self.organization_field)

        # Location field
        self.label_9 = QtWidgets.QLabel()
        self.label_9.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_9.setObjectName("label_9")
        self.label_9.setText("Location")

        self.location_combo = QtWidgets.QComboBox()
        self.location_combo.setMinimumSize(QtCore.QSize(400, 41))
        self.location_combo.setMaximumSize(QtCore.QSize(500, 41))
        self.location_combo.setObjectName("location_combo")
        self.form_layout.addRow(self.label_9, self.location_combo)

        # Username field
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Username")

        self.username = QtWidgets.QLineEdit()
        self.username.setMinimumSize(QtCore.QSize(400, 41))
        self.username.setMaximumSize(QtCore.QSize(500, 41))
        self.username.setObjectName("username")
        self.form_layout.addRow(self.label_3, self.username)

        # First Name field
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("First Name")

        self.firstname = QtWidgets.QLineEdit()
        self.firstname.setMinimumSize(QtCore.QSize(400, 41))
        self.firstname.setMaximumSize(QtCore.QSize(500, 41))
        self.firstname.setObjectName("firstname")
        self.form_layout.addRow(self.label_4, self.firstname)

        # Last Name field
        self.label_5 = QtWidgets.QLabel()
        self.label_5.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Last Name")

        self.lastname = QtWidgets.QLineEdit()
        self.lastname.setMinimumSize(QtCore.QSize(400, 41))
        self.lastname.setMaximumSize(QtCore.QSize(500, 41))
        self.lastname.setObjectName("lastname")
        self.form_layout.addRow(self.label_5, self.lastname)

        # Password field
        self.label_6 = QtWidgets.QLabel()
        self.label_6.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_6.setObjectName("label_6")
        self.label_6.setText("Password")

        self.password = QtWidgets.QLineEdit()
        self.password.setMinimumSize(QtCore.QSize(400, 41))
        self.password.setMaximumSize(QtCore.QSize(500, 41))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.form_layout.addRow(self.label_6, self.password)

        # Confirm Password field
        self.label_7 = QtWidgets.QLabel()
        self.label_7.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_7.setObjectName("label_7")
        self.label_7.setText("Confirm Password")

        self.confirmpassword = QtWidgets.QLineEdit()
        self.confirmpassword.setMinimumSize(QtCore.QSize(400, 41))
        self.confirmpassword.setMaximumSize(QtCore.QSize(500, 41))
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setObjectName("confirmpassword")
        self.form_layout.addRow(self.label_7, self.confirmpassword)

        # Add spacing before button
        buttonLayout = QVBoxLayout()
        buttonLayout.addSpacing(20)

        # Update button - centered
        self.update_button_layout = QHBoxLayout()
        self.update_button_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.update_button = QtWidgets.QPushButton()
        self.update_button.setMinimumSize(QtCore.QSize(391, 61))
        self.update_button.setMaximumSize(QtCore.QSize(500, 61))
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
        self.update_button.setText("UPDATE INFORMATION")
        self.update_button_layout.addWidget(self.update_button)

        buttonLayout.addLayout(self.update_button_layout)

        # Error message label - centered
        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        buttonLayout.addWidget(self.error_label)

        # Create a vertical layout to hold the form and buttons
        mainFormLayout = QVBoxLayout()
        mainFormLayout.addLayout(self.form_layout)
        mainFormLayout.addLayout(buttonLayout)

        # Add the main form layout to the form container
        self.form_container.addLayout(mainFormLayout)
        self.form_container.addStretch()

        # Add form container to main layout
        self.main_layout.addLayout(self.form_container)

        # Add spacer to push back button to bottom
        self.main_layout.addStretch()

        # Back button (bottom-left)
        self.back_layout = QHBoxLayout()

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
                background-color: rgb(240, 200, 150);
            }
        """)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")
        self.back_layout.addWidget(self.back_button)

        # Add spacer to push back button to left
        self.back_layout.addStretch()

        # Add back button layout to main layout
        self.main_layout.addLayout(self.back_layout)

        # Connect buttons to functions
        self.update_button.clicked.connect(self.update_user_info)
        self.back_button.clicked.connect(self.go_back)

        # Connect text change signals for real-time validation
        self.username.textChanged.connect(lambda: self.validate_field('username'))
        self.firstname.textChanged.connect(lambda: self.validate_field('firstname'))
        self.lastname.textChanged.connect(lambda: self.validate_field('lastname'))
        self.password.textChanged.connect(lambda: self.validate_field('password'))
        self.confirmpassword.textChanged.connect(lambda: self.validate_field('confirmpassword'))
        self.organization_field.textChanged.connect(lambda: self.validate_field('organization'))

        # Track changes to enable/disable update button
        self.username.textChanged.connect(self.track_changes)
        self.firstname.textChanged.connect(self.track_changes)
        self.lastname.textChanged.connect(self.track_changes)
        self.password.textChanged.connect(self.track_changes)
        self.confirmpassword.textChanged.connect(self.track_changes)
        self.organization_field.textChanged.connect(self.track_changes)
        self.location_combo.currentIndexChanged.connect(self.track_changes)

        # Set minimum size to ensure all content is visible
        Widget.setMinimumSize(1000, 700)

    def load_user_data(self):
        """Load user data from the database into the form fields"""
        if not self.user:
            return

        # Reset field styles
        for field in [self.username, self.firstname, self.lastname, self.password,
                      self.confirmpassword, self.organization_field]:
            field.setStyleSheet("")

        # Reset validation state
        for field in self.validators:
            self.validators[field] = True

        # Reset change tracking
        self.fields_changed = False

        # Clear any error messages
        self.error_label.setText("")

        # Hide or show organization field based on user type
        if self.user[6]:  # User is admin
            # For admin users, hide organization and location fields
            self.label_8.setVisible(False)
            self.organization_field.setVisible(False)
            self.label_9.setVisible(False)
            self.location_combo.setVisible(False)
        else:
            # For regular users, show organization and location fields
            self.label_8.setVisible(True)
            self.organization_field.setVisible(True)
            self.label_9.setVisible(True)
            self.location_combo.setVisible(True)

            # Load locations into combo box
            self.location_combo.clear()
            locations = self.database.get_all_locations()
            current_location_id = "QC"  # Default location

            if self.organization and len(self.organization) > 2:
                current_location_id = self.organization[2]

            # Populate locations dropdown
            selected_index = 0
            for i, location in enumerate(locations):
                self.location_combo.addItem(location[1], location[0])
                if location[0] == current_location_id:
                    selected_index = i

            # Set the selected location
            self.location_combo.setCurrentIndex(selected_index)

            # Load organization name if available
            if self.organization:
                print(f"Setting organization field to: {self.organization[1]}")
                self.organization_field.setText(str(self.organization[1]))  # organization name
            else:
                # Set a default value to prevent UI errors
                self.organization_field.setText("CARE Philippines")

        self.username.setText(self.user[1])  # username
        self.firstname.setText(self.user[2])  # firstname
        self.lastname.setText(self.user[3])  # lastname
        self.password.setText(self.user[4])  # password
        self.confirmpassword.setText(self.user[5])  # confirm password

        # Update button state
        self.update_update_button_state()

    def update_user_info(self):
        """Update user information in the database"""
        print("Update button clicked")

        # Show loading indicator
        self.error_label.setText("Updating information...")
        QtWidgets.QApplication.processEvents()

        username = self.username.text().strip()
        firstname = self.firstname.text().strip()
        lastname = self.lastname.text().strip()
        password = self.password.text()
        confirm_password = self.confirmpassword.text()

        print(
            f"Form data: username={username}, firstname={firstname}, lastname={lastname}, passwords match={password == confirm_password}")

        # Store user_id for later refresh
        user_id = self.user[0]

        # Update user in database
        try:
            success, error = self.database.update_user(user_id, username, firstname, lastname, password)

            if not success:
                self.error_label.setText(error)
                print(f"Database update failed: {error}")
                return

            print("User information updated successfully")

            # Update organization name if user is not admin
            if not self.user[6]:
                org_name = self.organization_field.text()
                print(f"Organization name: {org_name}")
                print(f"Current organization in DB: {self.organization}")

                # Get selected location ID
                location_id = self.location_combo.currentData()
                print(f"Selected location ID: {location_id}")

                if not location_id:
                    # Fallback to default if no location selected
                    location_id = "QC"

                try:
                    # First remove the old organization if it exists
                    print(f"Removing existing organization for user {user_id}")
                    self.database.cursor.execute(
                        "DELETE FROM org_info WHERE user_code = ?",
                        (user_id,)
                    )

                    # Then add the new organization
                    print(f"Adding new organization: {org_name}, user_code: {user_id}, location: {location_id}")
                    org_id, org_error = self.database.add_organization(
                        name=org_name,
                        user_code=user_id,
                        location_id=location_id
                    )

                    if org_error:
                        print(f"Error adding organization: {org_error}")
                        # Don't return, just log the error, but allow the user update to proceed
                    else:
                        print(f"Organization updated successfully with ID: {org_id}")

                    self.database.commit()
                except Exception as e:
                    print(f"Exception during organization update: {str(e)}")
                    # Don't stop the user update process for organization errors

            # Show success message with more details
            success_msg = QMessageBox(self.widget)
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setWindowTitle("Profile Updated")
            success_msg.setText("Your information has been updated successfully!")

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

            # Update the user object with new data - with error handling
            try:
                # Force a database refresh without caching
                self.database.connection.commit()

                # Explicitly get updated user data
                updated_user = self.database.get_user_by_id(user_id)
                print(f"After update - retrieved user data: {updated_user}")

                # Only update if we got a valid user back
                if updated_user:
                    self.user = updated_user

                    # Also update organization data if needed and user is not admin
                    if self.user and not self.user[6]:
                        try:
                            self.organization = self.database.get_user_organization(user_id)
                            print(f"Updated organization data: {self.organization}")
                        except Exception as org_err:
                            print(f"Error updating organization data: {str(org_err)}")
                            # Continue even if organization update fails
                else:
                    print("Warning: Could not retrieve updated user data")
            except Exception as user_err:
                print(f"Error updating user data: {str(user_err)}")
                # Continue even if we couldn't refresh the user data

            # Reset validation and change tracking
            self.load_user_data()

            # Go back to the appropriate menu - with additional safety check
            self.go_back()

        except Exception as e:
            print(f"Unexpected error during update: {str(e)}")
            self.error_label.setText(f"Error: {str(e)}")

    def go_back(self):
        """Go back to the appropriate menu based on user type"""
        if not self.user:
            # Safety check - if somehow user is None, go to login screen
            self.main_window.show_login_screen()
            return

        # Clear any error messages before navigating away
        self.error_label.setText("")

        # Get fresh user data from database to ensure it's updated
        try:
            # Force a database refresh
            self.database.refresh_connection()
            updated_user = self.database.get_user_by_id(self.user[0])

            if updated_user:
                self.user = updated_user
                print(f"Refreshed user data before returning to menu: {self.user}")
            else:
                print("Warning: Could not get updated user data")
        except Exception as e:
            print(f"Error refreshing user data: {str(e)}")

        if self.user[6]:  # User is admin
            self.main_window.show_admin_menu(self.user)
        else:
            self.main_window.show_user_menu(self.user)

    def validate_field(self, field_name):
        """Validate a specific field and update its visual state"""
        valid = False

        if field_name == 'username':
            text = self.username.text()
            if len(text) >= 3:
                # Check if username already exists and it's not the current user's username
                if self.user and text != self.user[1]:
                    existing_user = self.database.get_user_by_username(text)
                    if existing_user:
                        self.username.setStyleSheet("border: 2px solid red; background-color: #ffeeee;")
                        self.error_label.setText("Username already exists")
                        valid = False
                    else:
                        valid = True
                        self.username.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                        self.error_label.setText("")
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
            if not self.user or not self.user[6]:  # Only validate if not admin
                text = self.organization_field.text()
                if text:
                    valid = True
                    self.organization_field.setStyleSheet("border: 2px solid green; background-color: #eeffee;")
                else:
                    self.organization_field.setStyleSheet("border: 1px solid orange;")
            else:
                valid = True  # For admins, org field is not required

        # Update validator state
        self.validators[field_name] = valid

        # Update update button state
        self.update_update_button_state()

    def track_changes(self):
        """Track if any fields have been changed from their original values"""
        if not self.user:
            return

        # Compare current values with original values
        username_changed = self.username.text() != self.user[1]
        firstname_changed = self.firstname.text() != self.user[2]
        lastname_changed = self.lastname.text() != self.user[3]
        password_changed = self.password.text() != self.user[4]

        # Check organization change if it exists
        org_changed = False
        if not self.user[6] and self.organization:  # User is not admin and has organization
            org_changed = self.organization_field.text() != self.organization[1]

            # Check location change
            if self.location_combo.currentIndex() >= 0:
                location_id = self.location_combo.currentData()
                if location_id != self.organization[2]:
                    org_changed = True

        # Set fields_changed flag if any fields have changed
        self.fields_changed = (username_changed or firstname_changed or lastname_changed or
                               password_changed or org_changed)

        # Update button state
        self.update_update_button_state()

    def update_update_button_state(self):
        """Enable or disable update button based on validation state and changes"""
        # Always enable the update button regardless of validation state
        self.update_button.setEnabled(True)
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