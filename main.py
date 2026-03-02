import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from database.db_manager import DatabaseManager
from ui.login_screen import LoginScreen
from ui.signup_screen import SignupScreen
from ui.dashboards import AdminDashboard, UserDashboard

class CinemaApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        # Create screens once and keep them in the stack
        self.login_screen = LoginScreen(self.db_manager)
        self.signup_screen = SignupScreen(self.db_manager)
        
        # Connect signals
        self.login_screen.login_success.connect(self.route_user)
        self.login_screen.signup_requested.connect(self.show_signup)
        self.signup_screen.signup_success.connect(self.show_login)
        self.signup_screen.back_to_login.connect(self.show_login)
        
        # Add to stack
        self.addWidget(self.login_screen)
        self.addWidget(self.signup_screen)
        
        # Dashboard placeholders (created on-demand but managed)
        self.admin_dashboard = None
        self.user_dashboard = None

        self.setWindowTitle("Cinema Management System")
        self.resize(1100, 800)

    def show_signup(self):
        self.setCurrentWidget(self.signup_screen)

    def show_login(self):
        self.setCurrentWidget(self.login_screen)

    def route_user(self, user_data):
        if user_data['role'] == 'Admin':
            if not self.admin_dashboard:
                self.admin_dashboard = AdminDashboard(user_data, self.db_manager)
                self.admin_dashboard.logout_requested.connect(self.logout)
                self.addWidget(self.admin_dashboard)
            else:
                self.admin_dashboard.user_data = user_data
                self.admin_dashboard.init_ui() # Refresh data
            self.setCurrentWidget(self.admin_dashboard)
        else:
            if not self.user_dashboard:
                self.user_dashboard = UserDashboard(user_data, self.db_manager)
                self.user_dashboard.logout_requested.connect(self.logout)
                self.addWidget(self.user_dashboard)
            else:
                self.user_dashboard.user_data = user_data
                self.user_dashboard.init_ui() # Refresh data
            self.setCurrentWidget(self.user_dashboard)

    def logout(self):
        self.setCurrentWidget(self.login_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())
