from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class SignupScreen(QWidget):
    signup_success = pyqtSignal()
    back_to_login = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cinema Management System - Sign Up")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #121212;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 15px;
                border: 1px solid #333;
            }
        """)
        
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(30, 40, 30, 40)
        container_layout.setSpacing(15)
        container.setLayout(container_layout)

        title_label = QLabel("Create Account")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #e0e0e0; border: none;")
        container_layout.addWidget(title_label)

        self.fullname_input = self._create_input("Full Name")
        container_layout.addWidget(self.fullname_input)

        self.username_input = self._create_input("Username")
        container_layout.addWidget(self.username_input)

        self.password_input = self._create_input("Password", is_password=True)
        container_layout.addWidget(self.password_input)

        signup_btn = QPushButton("Sign Up")
        signup_btn.setFixedHeight(45)
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        signup_btn.clicked.connect(self.handle_signup)
        container_layout.addWidget(signup_btn)

        back_btn = QPushButton("Back to Login")
        back_btn.setStyleSheet("color: #3498db; border: none; background: none; text-decoration: underline;")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_to_login.emit)
        container_layout.addWidget(back_btn)

        layout.addWidget(container)

    def _create_input(self, placeholder, is_password=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(40)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background-color: #121212;
                border: 1px solid #333;
                border-radius: 5px;
                color: #e0e0e0;
            }
        """)
        return input_field

    def handle_signup(self):
        fullname = self.fullname_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not all([fullname, username, password]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if self.db_manager.create_user(username, password, "User", fullname):
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.signup_success.emit()
        else:
            QMessageBox.critical(self, "Error", "Username already exists.")
