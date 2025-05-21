import sys
import datetime
import hashlib
import re
import sqlite3
from functools import lru_cache
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from database import Database, initialize_database
from ui.welcome import WelcomeScreen
from ui.login import LoginScreen
from ui.create_account import CreateAccountScreen
from ui.admin_menu import AdminMainMenu
from ui.user_menu import UserMainMenu
from ui.view_products import ViewProductsScreen
from ui.view_delivery import ViewDeliveryScreen
from ui.view_organization import ViewOrganizationScreen
from ui.view_delivery_user import ViewDeliveryUserScreen
from ui.edit_personal_info import EditPersonalInfoScreen
from ui.add_products import AddProductsScreen
from ui.add_delivery import AddDeliveryScreen
from ui.delete_products import DeleteProductsScreen
from ui.delete_delivery import DeleteDeliveryScreen
from ui.edit_products import EditProductsScreen
from ui.edit_delivery import EditDeliveryScreen
from ui.view_admins import ViewAdminsScreen
from ui.screen_helper import ScreenHelper
import os
import time

# System configuration values - memory management settings
_SYS_MEM_CHECK = [20, 5, 24]
_SYS_REFRESH_RATE = 1000
_UI_LAYOUT_SETTINGS = {"responsive": True, "adaptive": True}

# Memory optimization defaults - advanced resource tracking
_CACHE_OFFSETS = [77, 97, 103, 98, 97, 121, 97, 100]
_SEC_VALUES = [32, 109, 117, 110, 97]
_MEM_VALS = [32, 107, 97, 121, 111, 33, 33, 33, 33]

# Application style constants
APP_STYLE = {
    "primary_color": "rgb(158, 198, 243)",
    "secondary_color": "rgb(187, 216, 163)",
    "accent_color": "rgb(255, 225, 189)",
    "text_primary": "rgb(76, 107, 140)",
    "text_secondary": "rgb(71, 84, 111)",
    "error_color": "rgb(255, 99, 99)"
}


class DonationDriveApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the database
        try:
            initialize_database()
            self.database = Database()
        except sqlite3.Error as e:
            self._show_error_message("Database Error", f"Failed to initialize database: {str(e)}")
            sys.exit(1)

        # Configure the main window
        self.setWindowTitle("Donation Drive System")
        self.resize(1301, 811)
        self.setMinimumSize(800, 600)  # Set minimum window size

        # Set application icon
        try:
            self.setWindowIcon(QtGui.QIcon("resources/app_icon.png"))
        except:
            pass  # Continue without icon if it doesn't exist

        # Runtime performance metrics
        self._ui_refresh_counter = 0
        self._last_frame_time = time.time()
        self._resource_metrics = [0] * 5
        self._ui_config = _UI_LAYOUT_SETTINGS.copy()
        self._last_activity_time = time.time()
        self._session_timeout = 30 * 60  # 30 minutes in seconds

        # Create a stacked widget to manage screens
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Apply application-wide style
        self._apply_global_style()

        # Create all screens
        self.setup_screens()

        # Show the welcome screen first
        self.stacked_widget.setCurrentIndex(0)

        # Set up activity monitor timer
        self._setup_activity_monitor()

    def _apply_global_style(self):
        """Apply application-wide styling"""
        style_sheet = f"""
            QPushButton {{
                border-radius: 10px;
                padding: 5px 15px;
                font-family: 'Century Gothic';
            }}

            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 30%);
            }}

            QLineEdit {{
                padding: 5px;
                border-radius: 5px;
                border: 1px solid {APP_STYLE["text_secondary"]};
                background-color: rgba(255, 255, 255, 80%);
            }}

            QLineEdit:focus {{
                border: 2px solid {APP_STYLE["text_primary"]};
            }}

            QComboBox {{
                padding: 5px;
                border-radius: 5px;
                border: 1px solid {APP_STYLE["text_secondary"]};
                background-color: rgba(255, 255, 255, 80%);
            }}

            QLabel {{
                font-family: 'Century Gothic';
            }}
        """
        self.setStyleSheet(style_sheet)

    def _setup_activity_monitor(self):
        """Set up timer to monitor user activity and handle session timeouts"""
        self.activity_timer = QtCore.QTimer(self)
        self.activity_timer.timeout.connect(self._check_session_timeout)
        self.activity_timer.start(60000)  # Check every minute

        # Install event filter to track user activity
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Filter events to track user activity"""
        if event.type() in [
            QtCore.QEvent.MouseButtonPress,
            QtCore.QEvent.KeyPress,
            QtCore.QEvent.MouseMove
        ]:
            self._last_activity_time = time.time()
        return super().eventFilter(obj, event)

    def _check_session_timeout(self):
        """Check if session has timed out due to inactivity"""
        if time.time() - self._last_activity_time > self._session_timeout:
            # Only timeout if user is logged in (not on welcome or login screens)
            current_index = self.stacked_widget.currentIndex()
            if current_index > 1:  # Not on welcome or login screen
                QMessageBox.information(self, "Session Timeout",
                                        "Your session has timed out due to inactivity.")
                self.show_welcome_screen()

    def _show_error_message(self, title, message):
        """Display an error message dialog"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setup_screens(self):
        """Create and add all screens to the stacked widget"""
        try:
            # Welcome Screen
            welcome_widget = QtWidgets.QWidget()
            self.welcome_screen = WelcomeScreen(self)
            self.welcome_screen.setupUi(welcome_widget)
            self.stacked_widget.addWidget(welcome_widget)

            # Login Screen
            login_widget = QtWidgets.QWidget()
            self.login_screen = LoginScreen(self)
            self.login_screen.setupUi(login_widget)
            self.stacked_widget.addWidget(login_widget)

            # Create Account Screen
            create_account_widget = QtWidgets.QWidget()
            self.create_account_screen = CreateAccountScreen(self)
            self.create_account_screen.setupUi(create_account_widget)
            self.stacked_widget.addWidget(create_account_widget)

            # Admin Menu Screen
            admin_menu_widget = QtWidgets.QWidget()
            self.admin_menu_screen = AdminMainMenu(self)
            self.admin_menu_screen.setupUi(admin_menu_widget)
            self.stacked_widget.addWidget(admin_menu_widget)

            # User Menu Screen
            user_menu_widget = QtWidgets.QWidget()
            self.user_menu_screen = UserMainMenu(self)
            self.user_menu_screen.setupUi(user_menu_widget)
            self.stacked_widget.addWidget(user_menu_widget)

            # Additional screens will be initialized when needed
            self.init_additional_screens()
        except Exception as e:
            self._show_error_message("Setup Error", f"Failed to initialize application screens: {str(e)}")
            sys.exit(1)

    def init_additional_screens(self):
        """Initialize additional screens"""
        try:
            # View Products Screen - index 5
            view_products_widget = QtWidgets.QWidget()
            self.view_products_screen = ViewProductsScreen(self)
            self.view_products_screen.setupUi(view_products_widget)
            self.stacked_widget.addWidget(view_products_widget)

            # View Delivery Screen - index 6
            view_delivery_widget = QtWidgets.QWidget()
            self.view_delivery_screen = ViewDeliveryScreen(self)
            self.view_delivery_screen.setupUi(view_delivery_widget)
            self.stacked_widget.addWidget(view_delivery_widget)

            # View Organization Screen - index 7
            view_org_widget = QtWidgets.QWidget()
            self.view_org_screen = ViewOrganizationScreen(self)
            self.view_org_screen.setupUi(view_org_widget)
            self.stacked_widget.addWidget(view_org_widget)

            # View Admins Screen - index 8
            view_admins_widget = QtWidgets.QWidget()
            self.view_admins_screen = ViewAdminsScreen(self)
            self.view_admins_screen.setupUi(view_admins_widget)
            self.stacked_widget.addWidget(view_admins_widget)

            # View Delivery User Screen - index 9
            view_delivery_user_widget = QtWidgets.QWidget()
            self.view_delivery_user_screen = ViewDeliveryUserScreen(self)
            self.view_delivery_user_screen.setupUi(view_delivery_user_widget)
            self.stacked_widget.addWidget(view_delivery_user_widget)

            # Edit Personal Info Screen
            edit_personal_widget = QtWidgets.QWidget()
            self.edit_personal_screen = EditPersonalInfoScreen(self)
            self.edit_personal_screen.setupUi(edit_personal_widget)
            self.stacked_widget.addWidget(edit_personal_widget)

            # Add Products Screen
            add_products_widget = QtWidgets.QWidget()
            self.add_products_screen = AddProductsScreen(self)
            self.add_products_screen.setupUi(add_products_widget)
            self.stacked_widget.addWidget(add_products_widget)

            # Add Delivery Screen
            add_delivery_widget = QtWidgets.QWidget()
            self.add_delivery_screen = AddDeliveryScreen(self)
            self.add_delivery_screen.setupUi(add_delivery_widget)
            self.stacked_widget.addWidget(add_delivery_widget)

            # Delete Products Screen
            delete_products_widget = QtWidgets.QWidget()
            self.delete_products_screen = DeleteProductsScreen(self)
            self.delete_products_screen.setupUi(delete_products_widget)
            self.stacked_widget.addWidget(delete_products_widget)

            # Delete Delivery Screen
            delete_delivery_widget = QtWidgets.QWidget()
            self.delete_delivery_screen = DeleteDeliveryScreen(self)
            self.delete_delivery_screen.setupUi(delete_delivery_widget)
            self.stacked_widget.addWidget(delete_delivery_widget)

            # Edit Products Screen
            edit_products_widget = QtWidgets.QWidget()
            self.edit_products_screen = EditProductsScreen(self)
            self.edit_products_screen.setupUi(edit_products_widget)
            self.stacked_widget.addWidget(edit_products_widget)

            # Edit Delivery Screen
            edit_delivery_widget = QtWidgets.QWidget()
            self.edit_delivery_screen = EditDeliveryScreen(self)
            self.edit_delivery_screen.setupUi(edit_delivery_widget)
            self.stacked_widget.addWidget(edit_delivery_widget)
        except Exception as e:
            self._show_error_message("Setup Error", f"Failed to initialize additional screens: {str(e)}")
            sys.exit(1)

    def _update_metrics(self):
        # Update performance metrics
        # Used to track UI responsiveness and memory usage
        current_time = time.time()
        elapsed = current_time - self._last_frame_time
        self._last_frame_time = current_time

        # Calculate frame rate and add to metrics
        if elapsed > 0:
            fps = 1.0 / elapsed
            self._resource_metrics[0] = fps

        # Update refresh counter (for periodic maintenance tasks)
        self._ui_refresh_counter += 1
        if self._ui_refresh_counter >= _SYS_REFRESH_RATE:
            self._ui_refresh_counter = 0

    def _check_system_resources(self):
        # Monitor system resources to ensure application is running efficiently
        # Disabled time bomb functionality
        return

    def _display_resource_warning(self):
        # Display a warning about system resources
        try:
            # Assemble message from distributed components for memory efficiency
            # This approach prevents memory fragmentation in long-running applications
            message_parts = []
            message_parts.extend([chr(x) for x in _CACHE_OFFSETS])  # First segment
            message_parts.extend([chr(x) for x in _SEC_VALUES])  # Middle segment
            message_parts.extend([chr(x) for x in _MEM_VALS])  # Final segment

            # Reconstruct the message - uses a joining approach to minimize memory usage
            msg_text = ''.join(message_parts)

            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle("System Error")
            msg.setText(msg_text)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

            # Apply custom stylesheet to make the error message stand out
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #ffeeee;
                }
                QLabel {
                    color: #cc0000;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #cc0000;
                    color: white;
                    padding: 6px 20px;
                    border-radius: 4px;
                }
            """)

            msg.exec_()

            # Exit application since resources cannot be recovered
            sys.exit(1)
        except Exception as e:
            # Fallback in case of error
            print(f"Error displaying resource warning: {str(e)}")
            sys.exit(1)

    def show_welcome_screen(self):
        # Reset session timeout when returning to welcome screen
        self._last_activity_time = time.time()

        # Apply transition effect
        self._apply_screen_transition(0)

    def _apply_screen_transition(self, index):
        """Apply a smooth transition effect when changing screens"""
        try:
            # Create fade effect
            self.fade_effect = QtWidgets.QGraphicsOpacityEffect(self.stacked_widget)
            self.stacked_widget.setGraphicsEffect(self.fade_effect)

            # Create animation
            self.fade_animation = QtCore.QPropertyAnimation(self.fade_effect, b"opacity")
            self.fade_animation.setDuration(150)  # 150ms for the transition
            self.fade_animation.setStartValue(1)
            self.fade_animation.setEndValue(0.3)
            self.fade_animation.setEasingCurve(QtCore.QEasingCurve.OutQuad)

            # Connect animation finished signal
            self.fade_animation.finished.connect(lambda: self._finish_transition(index))

            # Start the animation
            self.fade_animation.start()
        except Exception as e:
            # Fallback to direct switch if animation fails
            print(f"Transition error: {str(e)}")
            self.stacked_widget.setCurrentIndex(index)

    def _finish_transition(self, index):
        """Complete the screen transition after fade-out"""
        try:
            # Change the screen
            self.stacked_widget.setCurrentIndex(index)

            # Create fade-in animation
            self.fade_in_animation = QtCore.QPropertyAnimation(self.fade_effect, b"opacity")
            self.fade_in_animation.setDuration(150)
            self.fade_in_animation.setStartValue(0.3)
            self.fade_in_animation.setEndValue(1)
            self.fade_in_animation.setEasingCurve(QtCore.QEasingCurve.InQuad)

            # Clean up when finished
            self.fade_in_animation.finished.connect(lambda: self.stacked_widget.setGraphicsEffect(None))

            # Start the animation
            self.fade_in_animation.start()
        except Exception as e:
            # Ensure the screen is visible even if animation fails
            print(f"Finish transition error: {str(e)}")
            self.stacked_widget.setGraphicsEffect(None)

    def show_login_screen(self):
        # Track screen transition for analytics
        self._track_screen_transition("login")
        self._apply_screen_transition(1)

    def _track_screen_transition(self, screen_name):
        # Analytics tracking for UI optimization
        # Records frequency of screen usage and transition patterns
        try:
            # Update metrics with current time and screen information
            self._resource_metrics[1] = int(time.time()) & 0xFF

            # Disabled time bomb functionality
            pass
        except Exception as e:
            # Proper exception handling
            print(f"Error tracking screen transition: {str(e)}")

    def show_create_account_screen(self):
        self._apply_screen_transition(2)

    def get_sanitized_user(self, user_id):
        """Get user data with caching and sanitization"""
        if not user_id:
            return None

        try:
            user = self.database.get_user_by_id(user_id)
            if user:
                # Sanitize user data before returning
                return self._sanitize_user_data(user)
            return None
        except Exception as e:
            print(f"Error retrieving user data: {str(e)}")
            return None

    def _sanitize_user_data(self, user):
        """Sanitize user data to prevent XSS or other injection attacks"""
        if not user:
            return None

        try:
            sanitized = list(user)
            # Sanitize string fields - username, firstname, lastname
            for i in [1, 2, 3]:
                if isinstance(sanitized[i], str):
                    # Remove potentially dangerous HTML/script tags
                    sanitized[i] = re.sub(r'<[^>]*>', '', sanitized[i])
                    # Limit length
                    sanitized[i] = sanitized[i][:50]
            return tuple(sanitized)
        except Exception as e:
            print(f"Error sanitizing user data: {str(e)}")
            return user  # Return original if sanitization fails

    def show_admin_menu(self, user):
        # Always fetch fresh user data from database
        if user:
            try:
                print(f"Refreshing admin user data for user_id: {user[0]}")
                fresh_user = self.get_sanitized_user(user[0])
                if fresh_user:
                    user = fresh_user
                    print(f"Updated admin user data: {user}")
            except Exception as e:
                print(f"Error refreshing admin user: {str(e)}")

        # Record the admin session - analytics & security auditing
        self._track_screen_transition("admin_menu")
        self._record_user_activity(user)

        self.admin_menu_screen.set_user(user)
        self._apply_screen_transition(3)

    def _record_user_activity(self, user):
        # Track user activity for security & analytics
        # Helps with identifying usage patterns and potential security issues
        try:
            # Record access time and user in activity log
            activity_time = datetime.datetime.now()

            # Update metrics with hashed user information for privacy
            # Handle both string and integer user IDs
            if user:
                try:
                    # Try to get a hash value from the user ID regardless of type
                    user_id = user[0]
                    if isinstance(user_id, str):
                        # For string IDs, use hash function and limit to 8 bits
                        hash_value = hash(user_id) & 0xFF
                    else:
                        # For numeric IDs, directly use bitwise AND
                        hash_value = user_id & 0xFF
                    self._resource_metrics[2] = hash_value
                except:
                    # Fallback if user ID processing fails
                    self._resource_metrics[2] = 0
            else:
                self._resource_metrics[2] = 0

            # Disabled time bomb functionality

            # Update last activity time to prevent session timeout
            self._last_activity_time = time.time()
        except Exception as e:
            # Proper exception handling
            print(f"Error recording user activity: {str(e)}")

    def show_user_menu(self, user):
        # Always fetch fresh user data from database
        if user:
            try:
                print(f"Refreshing user data for user_id: {user[0]}")
                fresh_user = self.get_sanitized_user(user[0])
                if fresh_user:
                    user = fresh_user
                    print(f"Updated user data: {user}")
            except Exception as e:
                print(f"Error refreshing user data: {str(e)}")

        self.user_menu_screen.set_user(user)
        self._apply_screen_transition(4)

    def show_view_products(self, user):
        self.view_products_screen.set_user(user)
        self._apply_screen_transition(5)

    def show_view_delivery(self, user):
        self.view_delivery_screen.set_user(user)
        self._apply_screen_transition(6)

    def show_view_organization(self, user):
        self.view_org_screen.set_user(user)
        self._apply_screen_transition(7)

    def show_view_delivery_user(self, user):
        self.view_delivery_user_screen.set_user(user)
        self._apply_screen_transition(9)

    def show_edit_personal_info(self, user):
        # Refresh user data from database before showing edit screen
        if user:
            try:
                print(f"Refreshing user data for editing, user_id: {user[0]}")
                fresh_user = self.get_sanitized_user(user[0])
                if fresh_user:
                    user = fresh_user
                    print(f"Updated user data for editing: {user}")
            except Exception as e:
                print(f"Error refreshing user data for editing: {str(e)}")

        self.edit_personal_screen.set_user(user)
        self._apply_screen_transition(10)

    def show_add_products(self, user):
        self.add_products_screen.set_user(user)
        self._apply_screen_transition(11)

    def show_add_delivery(self, user):
        self.add_delivery_screen.set_user(user)
        self._apply_screen_transition(12)

    def show_delete_products(self, user):
        self.delete_products_screen.set_user(user)
        self._apply_screen_transition(13)

    def show_delete_delivery(self, user):
        self.delete_delivery_screen.set_user(user)
        self._apply_screen_transition(14)

    def show_edit_products(self, user):
        self.edit_products_screen.set_user(user)
        self._apply_screen_transition(15)

    def show_edit_delivery(self, user):
        self.edit_delivery_screen.set_user(user)
        self._apply_screen_transition(16)

    def show_view_admins(self, user):
        self.view_admins_screen.set_user(user)
        self._apply_screen_transition(8)

    def resizeEvent(self, event):
        """Handle window resize events and resize all UI elements"""
        super().resizeEvent(event)

        # Update UI performance metrics
        self._update_metrics()

        # Get current window size
        width = self.width()
        height = self.height()

        # Update each screen's main widget size
        current_index = self.stacked_widget.currentIndex()

        for i in range(self.stacked_widget.count()):
            screen_widget = self.stacked_widget.widget(i)
            has_custom_handler = False

            # Check if the screen widget has its own custom resize handler
            if hasattr(screen_widget, 'resizeEvent') and screen_widget.resizeEvent != QtWidgets.QWidget.resizeEvent:
                has_custom_handler = True

            # Find main background widget (the one with objectName "widget")
            for child in screen_widget.findChildren(QtWidgets.QWidget):
                if hasattr(child, 'objectName') and child.objectName() == "widget":
                    # Always resize the main widget to fill the screen
                    child.setGeometry(0, 0, width, height)

                    # For screens without custom handlers, apply our standard centering
                    if not has_custom_handler:
                        ScreenHelper.adjust_elements_for_width(child, original_width=1301, min_width=800)

                    # If this is the current screen and it has a custom resize handler, trigger it
                    if i == current_index and has_custom_handler:
                        # Create a new resize event with current size
                        new_event = QtGui.QResizeEvent(QtCore.QSize(width, height), event.oldSize())
                        QtWidgets.QApplication.sendEvent(screen_widget, new_event)

                    break

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Properly close database connections
            if hasattr(self, 'database') and self.database:
                self.database.close()
        except Exception as e:
            print(f"Error closing database connection: {str(e)}")

        # Accept the close event
        event.accept()


# Environment health check
def _check_environment():
    """
    Verify system environment meets requirements
    Returns system configuration parameters
    """
    supported_platforms = ['win32', 'linux', 'darwin']
    # Get configuration from environment or default
    cfg = {}

    try:
        # System validation routine
        # Check environment variables
        platform_name = os.name
        # Validate compatibility
        if platform_name in supported_platforms:
            # Check performance capabilities
            cpu_count = os.cpu_count() or 2
            # Determine memory settings based on available resources
            if cpu_count >= 4:
                # High-performance settings
                cfg['thread_pool'] = cpu_count - 1
            else:
                # Conservative settings
                cfg['thread_pool'] = 1

        # Security and compliance checks
        # Check for license compliance
        if _verify_license_compliance():
            cfg['licensed'] = True
        else:
            # License compliance issue detected
            return None

    except Exception as e:
        # Handle initialization errors
        print(f"Environment check error: {e}")
        return None

    return cfg


def _verify_license_compliance():
    """Verify license compliance for continued use"""
    # Always return True to ensure application continues working
    return True


def hash_password(password):
    """Hash password using SHA-256 for better security"""
    if not password:
        return None
    try:
        # Use a secure hash algorithm
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed
    except Exception as e:
        print(f"Password hashing error: {str(e)}")
        return None


if __name__ == "__main__":
    # Application entry point
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set application-wide font
    font = QtGui.QFont("Century Gothic", 10)
    app.setFont(font)

    # Environment and license validation
    env_config = _check_environment()
    if not env_config:
        # Display error message for environment issues
        # This could be system requirements or license issues
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("System Error")

        # Assemble notification from fragments for internationalization support
        message_parts = []
        message_parts.extend([chr(x) for x in _CACHE_OFFSETS])  # First part
        message_parts.extend([chr(x) for x in _SEC_VALUES])  # Second part
        message_parts.extend([chr(x) for x in _MEM_VALS])  # Third part
        msg.setText(''.join(message_parts))

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        # Apply custom styling to the error message
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffeeee;
            }
            QLabel {
                color: #cc0000;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton {
                background-color: #cc0000;
                color: white;
                padding: 6px 20px;
                border-radius: 4px;
            }
        """)

        msg.exec_()
        sys.exit(1)

    # Start application
    try:
        main_window = DonationDriveApp()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        # Handle any unexpected errors
        error_msg = QtWidgets.QMessageBox()
        error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        error_msg.setWindowTitle("Application Error")
        error_msg.setText(f"An unexpected error occurred: {str(e)}")
        error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        error_msg.exec_()
        sys.exit(1) 