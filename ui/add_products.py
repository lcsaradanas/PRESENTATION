from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import random
from ui.screen_helper import ScreenHelper


class AddProductsScreen(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = main_window.database
        self.user = None
        self.product_entries = []
        self.food_lists = []

    def set_user(self, user):
        self.user = user
        self.load_food_lists()
        # Always clear the form fields when screen is displayed
        if hasattr(self, 'product_entries') and self.product_entries:
            self.clear_form_fields()
        # The status label will be updated by clear_form_fields

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1350, 811)  # Make window slightly wider

        self.widget = QtWidgets.QWidget(Widget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1350, 811))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(158, 198, 243);}")
        self.widget.setObjectName("widget")

        # Title
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(430, 20, 490, 61))
        self.label.setStyleSheet("font: 30pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.label.setObjectName("label")
        self.label.setText("ADD PRODUCTS")

        # Subtitle
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(430, 80, 490, 31))
        self.label_2.setStyleSheet("font: 16pt \"Century Gothic\";color:\n"
                                   "rgb(71, 84, 111)")
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Add products to a food list")

        # Food List selection
        self.list_label = QtWidgets.QLabel(self.widget)
        self.list_label.setGeometry(QtCore.QRect(100, 130, 210, 31))
        self.list_label.setStyleSheet("font: 14pt \"Century Gothic\";")
        self.list_label.setObjectName("list_label")
        self.list_label.setText("SELECT FOOD LIST:")

        self.food_list_combo = QtWidgets.QComboBox(self.widget)
        self.food_list_combo.setGeometry(QtCore.QRect(320, 130, 630, 31))
        self.food_list_combo.setStyleSheet("font: 12pt \"Century Gothic\";")
        self.food_list_combo.setObjectName("food_list_combo")

        # Products Group Box - make it slightly wider
        self.products_box = QtWidgets.QGroupBox(self.widget)
        self.products_box.setGeometry(QtCore.QRect(100, 180, 1150, 451))
        self.products_box.setStyleSheet("QGroupBox{\n"
                                        "background-color: rgb(200, 220, 240);\n"
                                        "border: 2px solid rgb(76, 107, 140);\n"
                                        "border-radius: 10px;\n"
                                        "}\n")
        self.products_box.setTitle("")
        self.products_box.setObjectName("products_box")

        # Create product entry forms
        self.create_product_entries()

        # Food list status label - move it above the buttons and make it wider
        self.status_label = QtWidgets.QLabel(self.widget)
        self.status_label.setGeometry(QtCore.QRect(100, 640, 1150, 30))  # Positioned above buttons, full width
        self.status_label.setStyleSheet("font: 12pt \"Century Gothic\"; color:rgb(76, 107, 140)")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text
        self.status_label.setObjectName("status_label")
        self.status_label.setText("Products in form: 0/5")

        # Back button - move down slightly to account for status label above
        self.back_button = QtWidgets.QPushButton(self.widget)
        self.back_button.setGeometry(QtCore.QRect(390, 680, 161, 61))  # Moved down by 30 pixels
        self.back_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: rgb(255, 225, 189);
                font: 75 18pt "Century Gothic";
                border: 2px solid orange;
            }
            QPushButton:hover {
                background-color: rgb(240, 200, 150);
            }
        """)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("BACK")

        # Save All button - move down slightly to match back button
        self.save_button = QtWidgets.QPushButton(self.widget)
        self.save_button.setGeometry(QtCore.QRect(590, 680, 350, 61))  # Moved down by 30 pixels
        self.save_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #BBD8A3;
                font: 75 18pt "Century Gothic";
                border: 2px solid green;
            }
            QPushButton:hover {
                background-color: #A6C18F;
            }
        """)
        self.save_button.setObjectName("save_button")
        self.save_button.setText("SAVE ALL PRODUCTS")

        # Error message label
        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setGeometry(QtCore.QRect(440, 720, 471, 31))
        self.error_label.setStyleSheet("font: 75 italic 12pt \"Century Gothic\";color:red;")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")

        # Connect signals
        self.food_list_combo.currentIndexChanged.connect(self.food_list_changed)
        self.save_button.clicked.connect(self.save_products)
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

            # Center the title and subtitle
            center_x = int(parent_width / 2)
            self.label.setGeometry(QtCore.QRect(center_x - 245, 20, 490, 61))
            self.label_2.setGeometry(QtCore.QRect(center_x - 245, 80, 490, 31))

            # Adjust the products box width and center it
            box_width = min(parent_width - 100, 1150)  # Keep 50px margin on each side
            box_x = int((parent_width - box_width) / 2)
            self.products_box.setGeometry(QtCore.QRect(box_x, 180, int(box_width), 451))

            # Adjust status label to match products box
            self.status_label.setGeometry(QtCore.QRect(box_x, 640, int(box_width), 30))

            # Position buttons
            button_y = 680

            # Back button on left
            back_button_x = int(parent_width * 0.3 - 80)
            self.back_button.setGeometry(QtCore.QRect(back_button_x, button_y, 161, 61))

            # Save button on right
            save_button_x = int(parent_width * 0.7 - 175)
            self.save_button.setGeometry(QtCore.QRect(save_button_x, button_y, 350, 61))

            # Center error label
            error_label_x = int(center_x - 235)
            self.error_label.setGeometry(QtCore.QRect(error_label_x, 750, 471, 31))

            # Adjust food list selection controls
            list_label_x = box_x
            self.list_label.setGeometry(QtCore.QRect(list_label_x, 130, 210, 31))

            combo_width = int(box_width - 210 - 20)  # Subtract label width and some spacing
            combo_x = list_label_x + 220
            self.food_list_combo.setGeometry(QtCore.QRect(combo_x, 130, combo_width, 31))

            # Adjust form elements inside products box if needed
            self.adjust_product_entries(int(box_width))

    def adjust_product_entries(self, box_width):
        """Adjust the product entry fields based on available width"""
        if not self.product_entries:
            return

        # Calculate new widths for fields
        name_width = int((box_width - 260) * 0.35)  # 35% of available space

        for i, entry in enumerate(self.product_entries):
            y_offset = 20 + (i * 80)

            # Product Label (keep position)
            entry['name_field'].setGeometry(QtCore.QRect(170, y_offset, name_width, 30))

            # Adjust position of perishable label based on name field
            perishable_x = 180 + name_width + 10
            perishable_label_x = int(perishable_x)

            # Update perishable label position if it exists
            if 'perishable_label' in entry:
                entry['perishable_label'].setGeometry(QtCore.QRect(perishable_label_x, y_offset, 130, 30))

            # Update radio button positions
            radio_yes_x = int(perishable_x + 140)
            radio_no_x = int(perishable_x + 220)
            entry['perishable_yes'].setGeometry(QtCore.QRect(radio_yes_x, y_offset, 70, 30))
            entry['perishable_no'].setGeometry(QtCore.QRect(radio_no_x, y_offset, 70, 30))

            # Adjust quantity position
            quantity_x = int(perishable_x + 300)
            if 'quantity_label' in entry:
                entry['quantity_label'].setGeometry(QtCore.QRect(quantity_x, y_offset, 120, 30))

            quantity_field_x = int(quantity_x + 130)
            if 'quantity_field' in entry:
                entry['quantity_field'].setGeometry(QtCore.QRect(quantity_field_x, y_offset, 80, 30))

    def create_product_entries(self):
        """Create 5 product entry forms"""
        self.product_entries = []

        for i in range(5):
            y_offset = 20 + (i * 80)

            # Product ID (hidden in final UI)
            product_id = QtWidgets.QLabel(self.products_box)
            product_id.setGeometry(QtCore.QRect(20, y_offset, 120, 30))
            product_id.setStyleSheet("font: 10pt \"Century Gothic\";")
            product_id.setText(f"ID: {self.generate_product_id()}")
            product_id.setVisible(False)  # Hide ID in UI

            # Product Label
            product_label = QtWidgets.QLabel(self.products_box)
            product_label.setGeometry(QtCore.QRect(30, y_offset, 130, 30))
            product_label.setStyleSheet("font: 12pt \"Century Gothic\";")
            product_label.setText(f"PRODUCT {i + 1}:")

            # Name Field
            name_field = QtWidgets.QLineEdit(self.products_box)
            name_field.setGeometry(QtCore.QRect(170, y_offset, 360, 30))
            name_field.setPlaceholderText("Product Name")

            # Connect text changed event to update product count
            name_field.textChanged.connect(self.update_product_count_display)

            # Perishable Label
            perishable_label = QtWidgets.QLabel(self.products_box)
            perishable_label.setGeometry(QtCore.QRect(550, y_offset, 130, 30))
            perishable_label.setStyleSheet("font: 12pt \"Century Gothic\";")
            perishable_label.setText("PERISHABLE:")

            # Perishable Radio Buttons
            button_group = QtWidgets.QButtonGroup(self.products_box)

            yes_radio = QtWidgets.QRadioButton(self.products_box)
            yes_radio.setGeometry(QtCore.QRect(690, y_offset, 70, 30))
            yes_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
            yes_radio.setText("Yes")

            no_radio = QtWidgets.QRadioButton(self.products_box)
            no_radio.setGeometry(QtCore.QRect(770, y_offset, 70, 30))
            no_radio.setStyleSheet("font: 12pt \"Century Gothic\";")
            no_radio.setText("No")
            no_radio.setChecked(True)

            button_group.addButton(yes_radio)
            button_group.addButton(no_radio)

            # Quantity Label
            quantity_label = QtWidgets.QLabel(self.products_box)
            quantity_label.setGeometry(QtCore.QRect(860, y_offset, 120, 30))
            quantity_label.setStyleSheet("font: 12pt \"Century Gothic\";")
            quantity_label.setText("QUANTITY:")

            # Quantity Field
            quantity_field = QtWidgets.QSpinBox(self.products_box)
            quantity_field.setGeometry(QtCore.QRect(990, y_offset, 80, 30))
            quantity_field.setMinimum(1)
            quantity_field.setMaximum(10000)

            # Store references to all fields
            self.product_entries.append({
                'id_label': product_id,
                'product_label': product_label,
                'name_field': name_field,
                'perishable_label': perishable_label,
                'perishable_yes': yes_radio,
                'perishable_no': no_radio,
                'quantity_label': quantity_label,
                'quantity_field': quantity_field,
                'button_group': button_group
            })

    def generate_product_id(self):
        """Generate a random 6-digit product ID"""
        return random.randint(100000, 999999)

    def load_food_lists(self):
        """Load food lists from database"""
        if not self.user:
            return

        # Get all food lists
        self.food_lists = self.database.get_all_food_lists()

        # Clear and populate combo box
        self.food_list_combo.clear()

        # If there are no food lists yet, create the default 5
        if not self.food_lists:
            self.create_default_food_lists()
            self.food_lists = self.database.get_all_food_lists()

        # Add food lists to dropdown
        for food_list in self.food_lists:
            self.food_list_combo.addItem(food_list[1], food_list[0])

        # Initialize with first food list
        if self.food_lists:
            self.food_list_changed(0)

    def create_default_food_lists(self):
        """Create the 5 default food lists if they don't exist"""
        default_lists = [
            ("Food List 1 - For Closest Location", "Products for closest delivery locations"),
            ("Food List 2 - For Closer Location", "Products for closer delivery locations"),
            ("Food List 3 - For Close Location", "Products for moderately close delivery locations"),
            ("Food List 4 - For Farther Location", "Products for farther delivery locations"),
            ("Food List 5 - For Farthest Location", "Products for farthest delivery locations")
        ]

        for name, desc in default_lists:
            self.database.add_food_list(name, desc)

    def food_list_changed(self, index):
        """Handle food list selection change"""
        if index < 0 or not self.food_lists:
            return

        # Clear error message
        self.error_label.setText("")

        # Get selected food list ID
        food_list_id = self.food_list_combo.itemData(index)

        # Clear all entry fields
        self.clear_form_fields()

        # Update the status label (this is now handled by clear_form_fields)

    def save_products(self):
        """Save all products for the selected food list"""
        if not self.user:
            return

        food_list_id = self.food_list_combo.currentData()
        if not food_list_id:
            self.error_label.setText("Please select a food list")
            return

        # Get food list data to check how many products it has
        food_list_data = self.database.get_food_list(food_list_id)
        existing_products = []

        if food_list_data and 'products' in food_list_data:
            existing_products = food_list_data['products']

            # If already has 5 products, show warning
            if len(existing_products) >= 5:
                self.error_label.setText("This food list already has 5 products. Edit or delete existing products.")
                return

        # Validate all entries before processing
        empty_fields = []
        valid_products = []

        for i, entry in enumerate(self.product_entries):
            product_name = entry['name_field'].text().strip()

            if product_name:  # Only process entries with a name
                # Extract ID if it's an existing product, otherwise generate new 6-digit ID
                id_text = entry['id_label'].text()
                if "ID: " in id_text and len(id_text) > 4:  # Ensure there's an ID value
                    try:
                        product_id = int(id_text.replace("ID: ", "").strip())
                    except ValueError:
                        # If can't convert to int, generate new ID
                        product_id = self.generate_product_id()
                else:
                    product_id = self.generate_product_id()

                perishable = 1 if entry['perishable_yes'].isChecked() else 0
                quantity = entry['quantity_field'].value()

                if quantity <= 0:
                    self.error_label.setText(f"Product {i + 1}: Quantity must be greater than zero")
                    return

                valid_products.append((product_id, product_name, perishable, quantity))
            else:
                if entry['quantity_field'].value() > 1 or entry['perishable_yes'].isChecked():
                    empty_fields.append(i + 1)  # Track fields with missing names but other data

        # Alert about potentially incomplete entries
        if empty_fields and not valid_products:
            self.error_label.setText(f"Product(s) {', '.join(map(str, empty_fields))} missing name. No products added.")
            return
        elif empty_fields:
            # Just a warning but continue with valid products
            self.error_label.setText(
                f"Product(s) {', '.join(map(str, empty_fields))} missing name and will be skipped.")

        # Check if total products would exceed 5
        if len(existing_products) + len(valid_products) > 5:
            to_add = 5 - len(existing_products)
            self.error_label.setText(f"Can only add {to_add} more product(s) (limit 5 per list)")
            return

        if not valid_products:
            self.error_label.setText("Please enter at least one product name")
            return

        # Add each product to database
        added_count = 0
        updated_count = 0

        for product_id, name, perishable, quantity in valid_products:
            # Check if this is updating an existing product or adding a new one
            exists = False
            for product in existing_products:
                if product[0] == product_id:
                    # Update existing product
                    success, _ = self.database.update_product(product_id, name, perishable, quantity)
                    if success:
                        updated_count += 1
                    exists = True
                    break

            if not exists:
                # Insert the product with the specific product_id (not auto-generated)
                try:
                    # Use database directly instead of trying to access cursor
                    success, _ = self.database.add_product(name, perishable, quantity, product_id)
                    if success:
                        # Link to food list
                        self.database.add_product_to_food_list(food_list_id, product_id)
                        added_count += 1
                except Exception as e:
                    self.error_label.setText(f"Error adding product: {str(e)}")
                    return

        # Show success message with more detailed feedback
        message = ""
        if added_count > 0 and updated_count > 0:
            message = f"Added {added_count} new product(s) and updated {updated_count} existing product(s).\nFood List ID: {food_list_id}"
        elif added_count > 0:
            message = f"Added {added_count} new product(s) to the food list.\nFood List ID: {food_list_id}"
        elif updated_count > 0:
            message = f"Updated {updated_count} existing product(s) in the food list.\nFood List ID: {food_list_id}"

        if message:
            QMessageBox.information(self.widget, "Success", message)
            self.error_label.setText("")  # Clear any error messages

            # Clear the form completely instead of refreshing with data from database
            self.clear_form_fields()

            # Update status label is now handled by clear_form_fields
        else:
            self.error_label.setText("No products were added or updated")

    def clear_form_fields(self):
        """Clear all product entry fields completely"""
        for entry in self.product_entries:
            entry['name_field'].clear()
            entry['perishable_no'].setChecked(True)
            entry['quantity_field'].setValue(1)
            entry['id_label'].setText(f"ID: {self.generate_product_id()}")

        # Update status label to show 0 products
        self.update_product_count_display()

    def update_product_count_display(self):
        """Count filled products in form and update status label"""
        # Count products that have names filled in
        filled_products = 0
        for entry in self.product_entries:
            if entry['name_field'].text().strip():
                filled_products += 1

        # Get the total from database
        food_list_id = self.food_list_combo.currentData()
        if food_list_id:
            food_list_data = self.database.get_food_list(food_list_id)
            existing_products = []
            if food_list_data and 'products' in food_list_data:
                existing_products = food_list_data['products']

            # Update status label with both counts
            db_count = len(existing_products)
            self.status_label.setText(f"Products in form: {filled_products}/5 (Saved: {db_count}/5)")
        else:
            self.status_label.setText(f"Products in form: {filled_products}/5")

    def go_back(self):
        """Go back to the main menu"""
        self.main_window.show_admin_menu(self.user) 