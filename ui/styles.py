"""
Common UI styles for the Donation Drive Management System.
This module provides consistent styling for UI elements across all screens.
"""

# Background style for main widget
MAIN_BG_STYLE = """
    QWidget#widget {
        background-color: rgb(158, 198, 243);
    }
"""

# Title style
TITLE_STYLE = "font: 36pt \"Century Gothic\"; color: rgb(76, 107, 140);"

# Subtitle style
SUBTITLE_STYLE = "font: 16pt \"Century Gothic\"; color: rgb(71, 84, 111);"

# Label styles
LABEL_STYLE = "font: 12pt \"Century Gothic\";"
LABEL_BOLD_STYLE = "font: bold 12pt \"Century Gothic\";"
SELECT_LABEL_STYLE = "font: 14pt \"Century Gothic\";"

# ComboBox style
COMBOBOX_STYLE = """
    QComboBox { 
        font: 12pt "Century Gothic"; 
        padding: 5px; 
        border: 1px solid #76a5af;
        border-radius: 4px;
        background-color: white;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left-width: 1px;
        border-left-color: #76a5af;
        border-left-style: solid;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    QComboBox::down-arrow {
        width: 14px;
        height: 14px;
        background: transparent;
        border-top: 5px solid #76a5af;
        border-right: 5px solid transparent;
        border-left: 5px solid transparent;
        margin-right: 5px;
    }
"""

# Input field style
INPUT_STYLE = """
    QLineEdit { 
        font: 12pt "Century Gothic"; 
        padding: 5px; 
        border: 1px solid #76a5af;
        border-radius: 4px;
        background-color: white;
    }
"""

# Date Edit style
DATE_EDIT_STYLE = """
    QDateEdit { 
        font: 12pt "Century Gothic"; 
        padding: 5px; 
        border: 1px solid #76a5af;
        border-radius: 4px;
        background-color: white;
    }
"""

# Time Edit style
TIME_EDIT_STYLE = """
    QTimeEdit { 
        font: 12pt "Century Gothic"; 
        padding: 5px; 
        border: 1px solid #76a5af;
        border-radius: 4px;
        background-color: white;
    }
"""

# Button styles
PRIMARY_BUTTON_STYLE = """
    QPushButton {
        border-radius: 20px;
        background-color: rgb(187, 216, 163);
        font: 75 18pt "Century Gothic";
        border: none;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: rgb(200, 230, 180);
    }
"""

SECONDARY_BUTTON_STYLE = """
    QPushButton {
        border-radius: 20px;
        background-color: rgb(255, 225, 189);
        font: 75 16pt "Century Gothic";
        border: none;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: rgb(255, 235, 210);
    }
"""

FILTER_BUTTON_STYLE = """
    QPushButton {
        border-radius: 10px;
        background-color: rgb(187, 216, 163);
        font: 75 12pt "Century Gothic";
        border: none;
        padding: 4px 8px;
    }
    QPushButton:hover {
        background-color: rgb(200, 230, 180);
    }
"""

DELETE_BUTTON_STYLE = """
    QPushButton {
        border-radius: 20px;
        background-color: rgb(255, 100, 100);
        font: 75 18pt "Century Gothic";
        border: none;
        color: white;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: rgb(255, 120, 120);
    }
"""

# Table style
TABLE_STYLE = """
    QTableWidget {
        background-color: white;
        border: 1px solid #cccccc;
        border-radius: 4px;
        selection-background-color: #e6f2ff;
    }
    QHeaderView::section {
        background-color: #f0f0f0;
        border: 1px solid #cccccc;
        padding: 4px;
        font-weight: bold;
    }
    QTableWidget::item {
        padding: 4px;
        border-bottom: 1px solid #eeeeee;
    }
"""

# Selection box style
SELECTION_BOX_STYLE = """
    QGroupBox {
        background-color: rgb(220, 230, 240);
        border: 1px solid rgb(76, 107, 140);
        border-radius: 10px;
        margin-top: 5px;
        padding: 5px;
    }
"""

# Function to apply standard layout margins
def apply_standard_margins(layout, left=20, top=20, right=20, bottom=20):
    """Apply standard margins to a layout"""
    layout.setContentsMargins(left, top, right, bottom)
    layout.setSpacing(10) 