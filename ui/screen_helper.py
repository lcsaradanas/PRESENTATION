from PyQt5 import QtCore, QtWidgets


class ScreenHelper:
    """Helper class to adjust UI elements based on screen size"""

    @staticmethod
    def adjust_table_height(table_widget, screen_height, top_margin=250, bottom_margin=100):
        """
        Adjust table height based on screen height

        Args:
            table_widget: The QTableWidget to resize
            screen_height: The total screen height
            top_margin: Space above the table
            bottom_margin: Space below the table
        """
        new_height = screen_height - top_margin - bottom_margin
        if new_height > 200:  # Minimum table height
            table_widget.setFixedHeight(new_height)

    @staticmethod
    def resize_widget_for_screen(parent_widget):
        """
        Resize the widget to fill its parent

        Args:
            parent_widget: The parent widget to fill
        """
        if parent_widget.parent():
            parent_widget.setGeometry(0, 0, parent_widget.parent().width(), parent_widget.parent().height())

    @staticmethod
    def center_widget(widget, parent_width, original_x, original_width):
        """
        Center a widget horizontally

        Args:
            widget: The widget to center
            parent_width: The width of the parent container
            original_x: The original x position
            original_width: The original width of the widget
        """
        new_x = (parent_width - original_width) // 2
        geo = widget.geometry()
        widget.setGeometry(new_x, geo.y(), geo.width(), geo.height())

    @staticmethod
    def adjust_elements_for_width(widget, original_width=1301, min_width=800):
        """
        Adjust element positions based on screen width

        Args:
            widget: The parent widget
            original_width: The original design width
            min_width: The minimum width allowed
        """
        current_width = widget.width()

        # Only adjust if width is different from original design
        if current_width == original_width:
            return

        # Calculate scaling factor
        scale_factor = max(min_width, current_width) / original_width

        # Center adjustments
        center_offset = (current_width - original_width) / 2

        # Find title and subtitle labels - these should be centered
        for child in widget.findChildren(QtWidgets.QLabel):
            if hasattr(child, 'text'):
                text = child.text()
                # Skip if text is empty
                if not text:
                    continue

                # Only adjust centered title labels
                if (text.startswith("VIEW") or text.startswith("EDIT") or
                        text.startswith("ADD") or text.startswith("DELETE")):
                    # Get current geometry
                    geo = child.geometry()
                    x = geo.x()
                    y = geo.y()
                    width = geo.width()
                    height = geo.height()

                    # Center horizontally
                    new_x = int((current_width - width) / 2)

                    # Apply new geometry
                    child.setGeometry(new_x, y, width, height)

        # Find tables and adjust width
        for child in widget.findChildren(QtWidgets.QTableWidget):
            geo = child.geometry()
            x = geo.x()
            y = geo.y()
            width = geo.width()
            height = geo.height()

            # Scale width based on screen width
            new_width = int(min(current_width - 2 * x, width * scale_factor))

            # Center horizontally
            new_x = int((current_width - new_width) / 2)

            # Apply new geometry
            child.setGeometry(new_x, y, new_width, height)

        # Find group boxes and adjust width
        for child in widget.findChildren(QtWidgets.QGroupBox):
            geo = child.geometry()
            x = geo.x()
            y = geo.y()
            width = geo.width()
            height = geo.height()

            # Scale width based on screen width
            new_width = int(min(current_width - 40, width * scale_factor))

            # Center horizontally
            new_x = int((current_width - new_width) / 2)

            # Apply new geometry
            child.setGeometry(new_x, y, new_width, height)

        # Center buttons at the bottom
        for child in widget.findChildren(QtWidgets.QPushButton):
            geo = child.geometry()
            width = geo.width()
            y = geo.y()
            height = geo.height()

            # Only adjust buttons near the bottom (likely navigation buttons)
            if y > widget.height() * 0.7:
                if "BACK" in child.text():
                    # Left side with margin
                    new_x = int(current_width * 0.3 - width / 2)
                    child.setGeometry(new_x, y, width, height)
                elif "SAVE" in child.text() or "UPDATE" in child.text():
                    # Right side with margin
                    new_x = int(current_width * 0.7 - width / 2)
                    child.setGeometry(new_x, y, width, height)
                else:
                    # Center
                    new_x = int(current_width / 2 - width / 2)
                    child.setGeometry(new_x, y, width, height)

    @staticmethod
    def adjust_form_elements(widget, parent_width):
        """
        Adjust form elements to be centered and properly spaced

        Args:
            widget: The parent widget
            parent_width: The width of the parent container
        """
        # Find form containers (usually group boxes)
        group_boxes = widget.findChildren(QtWidgets.QGroupBox)

        for group_box in group_boxes:
            # Get the width of the group box
            box_width = group_box.width()

            # Center form fields inside the group box
            text_fields = group_box.findChildren(QtWidgets.QLineEdit)

            # Calculate maximum width for form fields
            if text_fields:
                # Get the original widths
                original_width = text_fields[0].width()
                # Calculate new width based on parent width
                new_width = min(original_width, int(box_width * 0.6))

                for field in text_fields:
                    # Get current position
                    geo = field.geometry()
                    field.setFixedWidth(new_width) 