from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from ui.screen_helper import ScreenHelper


class EditProductsScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.selected_product_id = None
        self.food_lists = []

    def set_user(self, user):
        self.user = user
        self.load_food_lists()
        self.load_products()

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
        self.label.setText("EDIT PRODUCT")

        # Subtitle
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(430, 100, 451, 41))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Select a product to edit")

        # Food List selection
        self.list_label = QtWidgets.QLabel(self.widget)
        self.list_label.setGeometry(QtCore.QRect(190, 150, 210, 31))
        self.list_label.setStyleSheet("font: 14pt \"Century Gothic\";")
        self.list_label.setObjectName("list_label")
        self.list_label.setText("SELECT FOOD LIST:")

        self.food_list_combo = QtWidgets.QComboBox(self.widget)
        self.food_list_combo.setGeometry(QtCore.QRect(400, 150, 611, 31))
        self.food_list_combo.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.food_list_combo.setObjectName("food_list_combo")

        # Search section - move down to make room for food list selection
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(190, 200, 121, 31))
        self.label_4.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("SEARCH:")

        # Search field - move down
        self.search_field = QtWidgets.QLineEdit(self.widget)
        self.search_field.setGeometry(QtCore.QRect(320, 200, 521, 31))
        self.search_field.setObjectName("search_field")

        # Apply filter button - move down
        self.apply_filter = QtWidgets.QPushButton(self.widget)
        self.apply_filter.setGeometry(QtCore.QRect(850, 200, 161, 31))
        self.apply_filter.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: rgb(187, 216, 163);
                font: 75 12pt "Century Gothic";
                border: 2px solid green;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: rgb(200, 230, 180);
            }
        """)
        self.apply_filter.setObjectName("apply_filter")
        self.apply_filter.setText("SEARCH")

        # Table widget for products - move down
        self.product_table = QtWidgets.QTableWidget(self.widget)
        self.product_table.setGeometry(QtCore.QRect(190, 250, 921, 200))
        self.product_table.setObjectName("product_table")
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(["ID", "Product Name", "Perishable", "Quantity"])

        # Make columns stretch to fill available space
        header = self.product_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        # Edit section - move down to account for table position
        self.edit_section = QtWidgets.QGroupBox(self.widget)
        self.edit_section.setGeometry(QtCore.QRect(190, 460, 921, 280))
        self.edit_section.setStyleSheet("QGroupBox{\n"
                                        "background-color: rgb(200, 220, 240);\n"
                                        "border: 2px solid rgb(76, 107, 140);\n"
                                        "border-radius: 10px;\n"
                                        "padding: 10px;\n"
                                        "}\n")
        self.edit_section.setTitle("")
        self.edit_section.setObjectName("edit_section")

        # Selected product label
        self.selected_label = QtWidgets.QLabel(self.edit_section)
        self.selected_label.setGeometry(QtCore.QRect(20, 20, 201, 31))
        self.selected_label.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.selected_label.setObjectName("selected_label")
        self.selected_label.setText("SELECTED PRODUCT:")

        self.selected_product_label = QtWidgets.QLabel(self.edit_section)
        self.selected_product_label.setGeometry(QtCore.QRect(230, 20, 671, 31))
        self.selected_product_label.setStyleSheet("font: 12pt \"Century Gothic\"; color: rgb(76, 107, 140)")
        self.selected_product_label.setObjectName("selected_product_label")
        self.selected_product_label.setText("None")

        # Product Name field
        self.label_3 = QtWidgets.QLabel(self.edit_section)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 151, 21))
        self.label_3.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("PRODUCT NAME")

        self.product_name = QtWidgets.QLineEdit(self.edit_section)
        self.product_name.setGeometry(QtCore.QRect(20, 100, 421, 41))
        self.product_name.setObjectName("product_name")

        # Perishable field
        self.label_5 = QtWidgets.QLabel(self.edit_section)
        self.label_5.setGeometry(QtCore.QRect(480, 70, 121, 21))
        self.label_5.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_5.setObjectName("label_5")
        self.label_5.setText("PERISHABLE")

        self.perishable_group = QtWidgets.QButtonGroup(self.edit_section)

        self.yes_radio = QtWidgets.QRadioButton(self.edit_section)
        self.yes_radio.setGeometry(QtCore.QRect(480, 100, 100, 30))
        self.yes_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.yes_radio.setObjectName("yes_radio")
        self.yes_radio.setText("Yes")

        self.no_radio = QtWidgets.QRadioButton(self.edit_section)
        self.no_radio.setGeometry(QtCore.QRect(600, 100, 100, 30))
        self.no_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.no_radio.setObjectName("no_radio")
        self.no_radio.setText("No")
        self.no_radio.setChecked(True)  # Default selection

        self.perishable_group.addButton(self.yes_radio)
        self.perishable_group.addButton(self.no_radio)

        # Quantity field
        self.label_6 = QtWidgets.QLabel(self.edit_section)
        self.label_6.setGeometry(QtCore.QRect(20, 160, 121, 21))
        self.label_6.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.label_6.setObjectName("label_6")
        self.label_6.setText("QUANTITY")

        self.quantity = QtWidgets.QSpinBox(self.edit_section)
        self.quantity.setGeometry(QtCore.QRect(20, 190, 421, 41))
        self.quantity.setMinimum(1)
        self.quantity.setMaximum(100000)
        self.quantity.setObjectName("quantity")

        # Update button
        self.update_button = QtWidgets.QPushButton(self.edit_section)
        self.update_button.setGeometry(QtCore.QRect(480, 190, 191, 61))
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
        self.back_button.setGeometry(QtCore.QRect(190, 760, 161, 41))
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
        self.error_label.setGeometry(QtCore.QRect(230, 150, 671, 31))
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")

        # Connect the buttons to their functions
        self.apply_filter.clicked.connect(self.apply_search)
        self.back_button.clicked.connect(self.go_back)
        self.update_button.clicked.connect(self.update_product)
        self.product_table.itemSelectionChanged.connect(self.on_selection_change)
        self.food_list_combo.currentIndexChanged.connect(self.food_list_changed)

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
            self.label_2.setGeometry(QtCore.QRect(int(center_x - 225), 100, 451, 41))

            # Calculate table and edit section positions
            available_height = parent_height - 220  # Adjust for title & top spacing

            margin_x = int(max(50, (parent_width - 1100) / 2))  # Min 50px, max 1100px width
            content_width = min(parent_width - 2 * margin_x, 1100)

            # Food list selector
            self.list_label.setGeometry(QtCore.QRect(margin_x, 150, 210, 31))
            combo_width = content_width - 220
            self.food_list_combo.setGeometry(QtCore.QRect(margin_x + 220, 150, combo_width, 31))

            # Search controls
            self.label_4.setGeometry(QtCore.QRect(margin_x, 200, 121, 31))
            search_width = content_width - 290
            self.search_field.setGeometry(QtCore.QRect(margin_x + 130, 200, search_width - 170, 31))
            self.apply_filter.setGeometry(QtCore.QRect(
                margin_x + 130 + search_width - 170 + 10, 200, 150, 31  # 10px gap
            ))

            # Calculate appropriate heights
            if available_height > 500:  # If enough vertical space
                table_height = int(available_height * 0.3)  # 30% for table
                edit_height = int(available_height * 0.5)  # 50% for edit box (reduced from 55%)
                spacing = 20  # Space between elements
            else:
                # Minimum heights for smaller screens
                table_height = 150
                edit_height = 280
                spacing = 10

            # Make sure heights are reasonable
            table_height = max(150, table_height)
            edit_height = max(280, edit_height)

            # Position elements
            table_y = 250
            edit_y = table_y + table_height + spacing

            # Table
            self.product_table.setGeometry(QtCore.QRect(margin_x, table_y, content_width, table_height))

            # Edit section
            self.edit_section.setGeometry(QtCore.QRect(margin_x, edit_y, content_width, edit_height))

            # Back button - position at bottom left with increased spacing
            back_button_y = edit_y + edit_height + 30  # Increased spacing from 'spacing' to fixed 30px

            # Safety check to keep button visible
            if back_button_y > parent_height - 60:
                back_button_y = parent_height - 60

            self.back_button.setGeometry(QtCore.QRect(margin_x, back_button_y, 161, 41))

    def load_food_lists(self):
        """Load food lists from database"""
        if not self.user:
            return

        # Get all food lists
        self.food_lists = self.database.get_all_food_lists()

        # Clear and populate combo box
        self.food_list_combo.clear()

        # Add an "All Products" option at the beginning
        self.food_list_combo.addItem("All Products", None)

        # Add food lists to dropdown
        for food_list in self.food_lists:
            self.food_list_combo.addItem(food_list[1], food_list[0])

    def food_list_changed(self, index):
        """Handle food list selection change"""
        # Reload products when food list changes
        self.load_products()

    def load_products(self):
        """Load products from database into the table"""
        if not self.user:
            return

        # Get selected food list ID (if any)
        food_list_id = self.food_list_combo.currentData() if hasattr(self, 'food_list_combo') else None

        # Get products - either all or filtered by food list
        if food_list_id:
            # Get products for this specific food list
            food_list_data = self.database.get_food_list(food_list_id)
            products = food_list_data['products'] if food_list_data and 'products' in food_list_data else []
        else:
            # Get all products
            products = self.database.get_all_products()

        # Clear the table
        self.product_table.setRowCount(0)

        # Get search term
        search_term = self.search_field.text().lower() if hasattr(self,
                                                                  'search_field') and self.search_field.text() else None

        # Populate the table
        row = 0
        for product in products:
            product_id = product[0]
            product_name = product[1]
            perishable = "Yes" if product[2] else "No"
            quantity = product[3]

            # If search term is specified, filter results
            if search_term and search_term not in product_name.lower():
                continue

            self.product_table.insertRow(row)
            self.product_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.product_table.setItem(row, 1, QTableWidgetItem(product_name))
            self.product_table.setItem(row, 2, QTableWidgetItem(perishable))
            self.product_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
            row += 1

    def apply_search(self):
        """Apply search filter to products table"""
        self.load_products()

    def on_selection_change(self):
        """Handle selection changes in the table"""
        selected_rows = self.product_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            product_id = self.product_table.item(row, 0).text()
            product_name = self.product_table.item(row, 1).text()
            perishable = self.product_table.item(row, 2).text()
            quantity = self.product_table.item(row, 3).text()

            self.selected_product_id = product_id
            self.selected_product_label.setText(f"ID: {product_id} - {product_name}")

            # Set form values
            self.product_name.setText(product_name)
            if perishable == "Yes":
                self.yes_radio.setChecked(True)
            else:
                self.no_radio.setChecked(True)
            self.quantity.setValue(int(quantity))
        else:
            self.selected_product_id = None
            self.selected_product_label.setText("None")
            self.product_name.clear()
            self.no_radio.setChecked(True)
            self.quantity.setValue(1)

    def update_product(self):
        """Update the selected product information"""
        if not self.selected_product_id:
            QMessageBox.warning(self.widget, "Warning", "Please select a product to update")
            return

        product_name = self.product_name.text().strip()
        perishable = 1 if self.yes_radio.isChecked() else 0
        quantity = self.quantity.value()

        if not product_name:
            QMessageBox.warning(self.widget, "Warning", "Product name cannot be empty")
            return

        success, error = self.database.update_product(
            self.selected_product_id,
            product_name,
            perishable,
            quantity
        )

        if success:
            QMessageBox.information(self.widget, "Success", "Product updated successfully!")
            # Reset selection
            self.selected_product_id = None
            self.selected_product_label.setText("None")
            self.product_name.clear()
            self.no_radio.setChecked(True)
            self.quantity.setValue(1)
            # Refresh the product list
            self.load_products()
        else:
            QMessageBox.critical(self.widget, "Error", f"Failed to update product: {error}")

    def go_back(self):
        """Go back to the main menu"""
        self.main_window.show_admin_menu(self.user)
