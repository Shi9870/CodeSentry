# resources/styles.py

# Define the QSS styles for the Dark Theme
# Note: Global font size settings are handled in main.py to avoid QFont warnings.

DARK_THEME_QSS = """
    /* Main Window Background */
    QMainWindow { background-color: #1e1e1e; }
    
    /* General Widget Settings */
    QWidget { 
        font-family: 'Segoe UI', 'Microsoft JhengHei', sans-serif; 
        color: #e0e0e0; 
    }
    
    /* Sidebar Styling */
    #Sidebar { 
        background-color: #252525; 
        border-right: 1px solid #333; 
    }
    #AppTitle { 
        font-size: 22px; 
        font-weight: bold; 
        color: #ffffff; 
        margin-bottom: 10px; 
    }
    #PathLabel { 
        color: #888; 
        font-size: 12px; 
    }
    
    /* ComboBox (Language Selector) Styling */
    QComboBox {
        background-color: #3a3a3a;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px;
        color: white;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 0px;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QComboBox QAbstractItemView {
        background-color: #3a3a3a;
        color: white;
        selection-background-color: #2ecc71;
        border: 1px solid #555;
    }

    /* General Button Styling */
    QPushButton { 
        background-color: #3a3a3a; 
        border: 1px solid #555; 
        border-radius: 4px; 
        padding: 8px; 
        color: white; 
    }
    QPushButton:hover { 
        background-color: #4a4a4a; 
    }
    
    /* Action Button (Start/Stop) Specifics */
    #ActionButton { 
        background-color: #2ecc71; 
        border: none; 
        font-weight: bold; 
        padding: 12px; 
    }
    #ActionButton:hover { 
        background-color: #27ae60; 
    }
    /* Red color when scanning is active */
    #ActionButton[state="stop"] { 
        background-color: #e74c3c; 
    }
    #ActionButton[state="stop"]:hover { 
        background-color: #c0392b; 
    }

    /* Tab Widget Styling */
    QTabWidget::pane { 
        border: 1px solid #333; 
        background: #1e1e1e; 
    }
    QTabBar::tab { 
        background: #2b2b2b; 
        color: #888; 
        padding: 10px 20px; 
        border-top-left-radius: 4px; 
        border-top-right-radius: 4px; 
        margin-right: 2px; 
    }
    QTabBar::tab:selected { 
        background: #1e1e1e; 
        color: white; 
        border-bottom: 2px solid #2ecc71; 
    }
    
    /* Table View Styling */
    QTableView { 
        background-color: #1e1e1e; 
        border: none; 
        selection-background-color: #2c3e50; 
    }
    QHeaderView::section { 
        background-color: #252525; 
        color: #bbb; 
        padding: 6px; 
        border: none; 
        font-weight: bold; 
    }
    
    /* Progress Bar Styling */
    QProgressBar { 
        border: 1px solid #444; 
        border-radius: 4px; 
        text-align: center; 
        background-color: #252525; 
        color: white; 
        font-weight: bold;
    }
    QProgressBar::chunk { 
        background-color: #3498db; 
    }
"""