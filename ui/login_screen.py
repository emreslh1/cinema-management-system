from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

class LoginScreen(QWidget):
    login_success = pyqtSignal(dict)
    signup_requested = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cinema Management System - Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #121212;")
        
        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Main container frame for styling
        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)
        container.setGraphicsEffect(None)
        container.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 15px;
                border: 1px solid #333;
            }
        """)
        
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(30, 40, 30, 40)
        container_layout.setSpacing(20)
        container.setLayout(container_layout)

        # Title
        title_label = QLabel("Cinema Login")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #e0e0e0; border: none;")
        container_layout.addWidget(title_label)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background-color: #121212;
                border: 1px solid #333;
                border-radius: 5px;
                font-size: 14px;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        container_layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background-color: #121212;
                border: 1px solid #333;
                border-radius: 5px;
                font-size: 14px;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        container_layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(45)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(login_btn)

        signup_btn = QPushButton("Don't have an account? Sign Up")
        signup_btn.setStyleSheet("color: #3498db; border: none; background: none; text-decoration: underline;")
        signup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        signup_btn.clicked.connect(self.signup_requested.emit)
        container_layout.addWidget(signup_btn)

        layout.addWidget(container)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        user_data = self.db_manager.authenticate_user(username, password)
        if user_data:
            self.login_success.emit(user_data)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
