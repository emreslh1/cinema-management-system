from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, 
                             QLineEdit, QComboBox, QFileDialog, QScrollArea, QGridLayout,
                             QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import os

class DashboardBase(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user_data, db_manager):
        super().__init__()
        self.user_data = user_data
        self.db_manager = db_manager
        self.apply_dark_theme()
        self.init_ui()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 8px;
                color: #e0e0e0;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #3498db;
            }
            QLineEdit, QComboBox, QTableWidget {
                background-color: #1e1e1e;
                border: 1px solid #333;
                padding: 5px;
                color: #e0e0e0;
                border-radius: 3px;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QTabWidget::pane {
                border: 1px solid #333;
            }
            QTabBar::tab {
                background: #1e1e1e;
                padding: 10px;
                color: #e0e0e0;
            }
            QTabBar::tab:selected {
                background: #333;
            }
            QScrollArea {
                border: none;
                background-color: #121212;
            }
            QMessageBox {
                background-color: #1e1e1e;
            }
        """)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Header
        header = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedWidth(100)
        logout_btn.clicked.connect(self.logout_requested.emit)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(logout_btn)
        
        self.layout.addLayout(header)
        self.layout.addSpacing(20)

class AdminDashboard(DashboardBase):
    def init_ui(self):
        super().init_ui()
        self.setWindowTitle("Admin Dashboard")
        self.title_label.setText(f"Admin: {self.user_data['username']}")

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Tab 1: User Management
        self.user_tab = QWidget()
        self.user_tab_layout = QVBoxLayout()
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Full Name", "Role"])
        self.load_users()
        self.user_tab_layout.addWidget(self.user_table)
        self.user_tab.setLayout(self.user_tab_layout)
        self.tabs.addTab(self.user_tab, "User Management")

        # Tab 2: Content Management (Grid + Form)
        self.content_tab = QWidget()
        self.content_tab_layout = QHBoxLayout()
        
        # Left Panel: Form and List
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: #1e1e1e; border-radius: 10px; border: 1px solid #333; }")
        self.form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.plot_input = QLineEdit()
        self.release_input = QLineEdit()
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("10.0")
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Movie", "TV Series"])
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["Action", "Drama", "Comedy", "Science Fiction", "Horror", "Romance", "Documentary", "Animation"])
        self.duration_input = QLineEdit()
        self.image_path_label = QLabel("No image selected")
        self.image_path = ""
        
        select_img_btn = QPushButton("Select Image")
        select_img_btn.clicked.connect(self.select_image)
        
        self.add_btn = QPushButton("Add Content")
        self.add_btn.clicked.connect(self.add_content)
        self.add_btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 10px;")

        self.form_layout.addRow("Title:", self.title_input)
        self.form_layout.addRow("Type:", self.type_combo)
        self.form_layout.addRow("Genre:", self.genre_combo)
        self.form_layout.addRow("Duration:", self.duration_input)
        self.form_layout.addRow("Release Date:", self.release_input)
        self.form_layout.addRow("Price ($):", self.price_input)
        self.form_layout.addRow("Plot:", self.plot_input)
        self.form_layout.addRow("Image:", select_img_btn)
        self.form_layout.addRow("", self.image_path_label)
        self.form_layout.addRow(self.add_btn)
        form_frame.setLayout(self.form_layout)
        left_layout.addWidget(form_frame)
        
        self.content_table = QTableWidget()
        self.content_table.setColumnCount(7)
        self.content_table.setHorizontalHeaderLabels(["ID", "Title", "Type", "Genre", "Dur", "Upd", "Del"])
        left_layout.addWidget(self.content_table)
        left_panel.setLayout(left_layout)
        
        # Right Panel: Visual Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("<b>Visual Grid Preview</b>"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.admin_grid_content = QWidget()
        self.admin_grid_layout = QGridLayout(self.admin_grid_content)
        scroll.setWidget(self.admin_grid_content)
        right_layout.addWidget(scroll)
        right_panel.setLayout(right_layout)
        
        self.content_tab_layout.addWidget(left_panel, 1)
        self.content_tab_layout.addWidget(right_panel, 1)
        self.content_tab.setLayout(self.content_tab_layout)
        self.tabs.addTab(self.content_tab, "Content Management")
        
        self.load_content_list()

    def load_users(self):
        users = self.db_manager.get_all_users()
        self.user_table.setRowCount(len(users))
        for i, user in enumerate(users):
            for j, val in enumerate(user):
                self.user_table.setItem(i, j, QTableWidgetItem(str(val)))

    def load_content_list(self):
        contents = self.db_manager.get_all_contents()
        self.content_table.setRowCount(len(contents))
        
        # Clear Grid
        for i in reversed(range(self.admin_grid_layout.count())): 
            widget = self.admin_grid_layout.itemAt(i).widget()
            if widget: 
                widget.setParent(None)
                widget.deleteLater()

        for i, content in enumerate(contents):
            # Fill Table
            for j in range(5):
                self.content_table.setItem(i, j, QTableWidgetItem(str(content[j])))
            
            c_id = content[0]
            
            # Create Update button with proper closure
            update_btn = QPushButton("Update")
            update_btn.clicked.connect(lambda checked=False, c=content: self.fill_update_form(c))
            self.content_table.setCellWidget(i, 5, update_btn)

            # Create Delete button with proper closure
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
            delete_btn.clicked.connect(lambda checked=False, id=c_id: self.delete_content_action(id))
            self.content_table.setCellWidget(i, 6, delete_btn)
            
            # Fill Grid
            card = self.create_preview_card(content)
            self.admin_grid_layout.addWidget(card, i // 2, i % 2)

    def create_preview_card(self, content):
        card = QFrame()
        card.setFixedSize(180, 280)
        card.setStyleSheet("QFrame { background: white; border: 1px solid #ccc; border-radius: 8px; }")
        layout = QVBoxLayout()
        
        img = QLabel()
        img.setFixedSize(160, 180)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if content[5] and os.path.exists(content[5]):
            pixmap = QPixmap(content[5])
            img.setPixmap(pixmap.scaled(160, 180, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            img.setText("No Image")
            
        title = QLabel(content[1])
        title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(img)
        layout.addWidget(title)
        layout.addStretch()
        card.setLayout(layout)
        return card

    def fill_update_form(self, content):
        # Ensure content is a tuple/list with expected length
        if not content or len(content) < 9:
            QMessageBox.critical(self, "Error", "Invalid content data")
            return
            
        self.current_update_id = content[0]
        self.title_input.setText(str(content[1]) if content[1] else "")
        self.type_combo.setCurrentText(str(content[2]) if content[2] else "Movie")
        self.genre_combo.setCurrentText(str(content[3]) if content[3] else "Action")
        self.duration_input.setText(str(content[4]) if content[4] else "")
        self.image_path = content[5] if content[5] else ""
        self.image_path_label.setText(self.image_path.split("/")[-1] if self.image_path else "No image selected")
        self.plot_input.setText(str(content[6]) if content[6] else "")
        self.release_input.setText(str(content[7]) if content[7] else "")
        try:
            self.price_input.setText(str(float(content[8])) if content[8] else "10.0")
        except:
            self.price_input.setText("10.0")
            
        self.add_btn.setText("Save Changes")
        try:
            self.add_btn.clicked.disconnect()
        except: 
            pass
        self.add_btn.clicked.connect(self.save_update)

    def save_update(self):
        # Validate update_id exists
        if not hasattr(self, 'current_update_id') or self.current_update_id is None:
            QMessageBox.critical(self, "Error", "No content selected for update")
            return
            
        # Get and strip all input values
        title = self.title_input.text().strip()
        c_type = self.type_combo.currentText()
        genre = self.genre_combo.currentText()
        duration = self.duration_input.text().strip()
        plot = self.plot_input.text().strip()
        release = self.release_input.text().strip()
        price_text = self.price_input.text().strip()
        
        # Validation: Check mandatory fields
        errors = []
        
        if not title:
            errors.append("Title is required")
        if not duration:
            errors.append("Duration is required")
        if not release:
            errors.append("Release Date is required")
        if not price_text:
            errors.append("Price is required")
        
        # Validation: Check price format
        price = 0.0
        if price_text:
            try:
                price = float(price_text)
                if price < 0:
                    errors.append("Price cannot be negative")
                elif price > 1000:
                    errors.append("Price seems too high (max $1000)")
            except ValueError:
                errors.append("Price must be a valid number (e.g., 12.50)")
        
        # Validation: Check release date format
        if release:
            import re
            if not re.match(r'^\d{4}(-\d{2}(-\d{2})?)?$', release):
                errors.append("Release Date should be in format: YYYY or YYYY-MM or YYYY-MM-DD")
        
        # Show errors if any
        if errors:
            error_msg = "Please fix the following errors:\n\n" + "\n".join(f"• {e}" for e in errors)
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        try:
            self.db_manager.update_content(
                self.current_update_id, title, c_type, genre, duration, 
                self.image_path, plot, release, price
            )
            QMessageBox.information(self, "Success", f"'{title}' has been updated successfully!")
            
            # Reset form
            self.title_input.clear()
            self.duration_input.clear()
            self.plot_input.clear()
            self.release_input.clear()
            self.price_input.clear()
            self.image_path = ""
            self.image_path_label.setText("No image selected")
            self.add_btn.setText("Add Content")
            self.current_update_id = None
            try:
                self.add_btn.clicked.disconnect()
            except: 
                pass
            self.add_btn.clicked.connect(self.add_content)
            self.load_content_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update content: {str(e)}")

    def delete_content_action(self, content_id):
        # Ensure content_id is an integer
        try:
            cid = int(content_id)
        except (ValueError, TypeError):
            QMessageBox.critical(self, "Error", "Invalid content ID")
            return
            
        reply = QMessageBox.question(self, "Delete Content", "Are you sure you want to delete this content?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_content(cid)
                QMessageBox.information(self, "Success", "Content deleted successfully!")
                self.load_content_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete content: {str(e)}")

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.image_path_label.setText(file_path.split("/")[-1])

    def add_content(self):
        # Get and strip all input values
        title = self.title_input.text().strip()
        c_type = self.type_combo.currentText()
        genre = self.genre_combo.currentText()
        duration = self.duration_input.text().strip()
        plot = self.plot_input.text().strip()
        release = self.release_input.text().strip()
        price_text = self.price_input.text().strip()
        
        # Validation: Check mandatory fields
        errors = []
        
        if not title:
            errors.append("Title is required")
        if not duration:
            errors.append("Duration is required")
        if not release:
            errors.append("Release Date is required")
        if not price_text:
            errors.append("Price is required")
        
        # Validation: Check price format
        price = 0.0
        if price_text:
            try:
                price = float(price_text)
                if price < 0:
                    errors.append("Price cannot be negative")
                elif price > 1000:
                    errors.append("Price seems too high (max $1000)")
            except ValueError:
                errors.append("Price must be a valid number (e.g., 12.50)")
        
        # Validation: Check release date format (basic check)
        if release:
            import re
            if not re.match(r'^\d{4}(-\d{2}(-\d{2})?)?$', release):
                errors.append("Release Date should be in format: YYYY or YYYY-MM or YYYY-MM-DD")
        
        # Show errors if any
        if errors:
            error_msg = "Please fix the following errors:\n\n" + "\n".join(f"• {e}" for e in errors)
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        # All validations passed - add content
        try:
            self.db_manager.add_content(title, c_type, genre, duration, self.image_path, plot, release, price)
            QMessageBox.information(self, "Success", f"'{title}' has been added successfully!")
            
            # Clear form
            self.title_input.clear()
            self.duration_input.clear()
            self.plot_input.clear()
            self.release_input.clear()
            self.price_input.clear()
            self.image_path = ""
            self.image_path_label.setText("No image selected")
            self.load_content_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add content: {str(e)}")

class UserDashboard(DashboardBase):
    def init_ui(self):
        super().init_ui()
        self.setWindowTitle("User Dashboard")
        self.title_label.setText(f"Welcome, {self.user_data['username']}")

        # Search and Filter Bar
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search movies or series...")
        self.search_input.setFixedHeight(35)
        self.search_input.textChanged.connect(self.load_contents)
        
        self.genre_filter = QComboBox()
        self.genre_filter.addItems(["All Genres", "Action", "Drama", "Comedy", "Science Fiction", "Horror", "Romance", "Documentary", "Animation"])
        self.genre_filter.setFixedHeight(35)
        self.genre_filter.currentTextChanged.connect(self.load_contents)
        
        filter_layout.addWidget(self.search_input, 3)
        filter_layout.addWidget(self.genre_filter, 1)
        self.layout.addLayout(filter_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        self.layout.addWidget(scroll)
        
        self.load_contents()

    def load_contents(self):
        # Clear existing layout
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget: widget.deleteLater()

        search_text = self.search_input.text().lower()
        selected_genre = self.genre_filter.currentText()

        contents = self.db_manager.get_all_contents()
        
        # Apply filtering
        filtered_contents = []
        for content in contents:
            title_match = search_text in content[1].lower()
            genre_match = selected_genre == "All Genres" or content[3] == selected_genre
            
            if title_match and genre_match:
                filtered_contents.append(content)

        for i, content in enumerate(filtered_contents):
            card = self.create_content_card(content)
            self.grid_layout.addWidget(card, i // 4, i % 4)

    def create_content_card(self, content):
        card = QFrame()
        card.setFixedSize(220, 380)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        # Oval structure with 20px border-radius and red glow on hover
        card.setStyleSheet("""
            QFrame { 
                background-color: #1e1e1e; 
                border: 1px solid #333; 
                border-radius: 20px; 
                padding: 10px;
            }
            QFrame:hover {
                border: 2px solid #e74c3c;
                background-color: #252525;
            }
        """)
        # Make the card clickable
        card.mousePressEvent = lambda event, c=content: self.show_movie_details(c)
        
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Image with oval corners
        img_label = QLabel()
        img_label.setFixedSize(180, 240)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("border-radius: 15px; background-color: #121212;")
        if content[5] and os.path.exists(content[5]):
            pixmap = QPixmap(content[5])
            img_label.setPixmap(pixmap.scaled(180, 240, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        else:
            img_label.setText("No Image")
        
        title_label = QLabel(content[1])
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_label = QLabel(f"{content[2]} | {content[3]}")
        info_label.setStyleSheet("color: #aaa; font-size: 11px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        duration_label = QLabel(f"⏱ {content[4]}")
        duration_label.setStyleSheet("color: #888; font-size: 10px;")
        duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(img_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(info_label)
        card_layout.addWidget(duration_label)
        card.setLayout(card_layout)
        return card

    def show_movie_details(self, content):
        # Create a detailed view overlay or new screen
        details_window = QWidget()
        details_window.setWindowTitle(f"Details - {content[1]}")
        details_window.setFixedSize(700, 500)
        details_window.setStyleSheet("background-color: #121212; color: #e0e0e0;")
        
        layout = QHBoxLayout()
        details_window.setLayout(layout)
        
        # Left side: Poster
        poster_label = QLabel()
        poster_label.setFixedSize(300, 450)
        if content[5] and os.path.exists(content[5]):
            pixmap = QPixmap(content[5])
            poster_label.setPixmap(pixmap.scaled(300, 450, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            poster_label.setText("No Image")
            poster_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #333;")
        
        # Right side: Info
        info_panel = QWidget()
        info_layout = QVBoxLayout()
        info_panel.setLayout(info_layout)
        
        title = QLabel(content[1])
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setWordWrap(True)
        
        meta = QLabel(f"📅 Release: {content[7]}  |  🏷 Category: {content[3]}")
        meta.setStyleSheet("color: #aaa;")
        
        price = QLabel(f"💰 Ticket Price: ${content[8]}")
        price.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        price.setStyleSheet("color: #2ecc71;")
        
        plot_title = QLabel("Plot Summary:")
        plot_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        plot = QLabel(content[6] if content[6] else "No plot available.")
        plot.setWordWrap(True)
        plot.setStyleSheet("color: #bbb;")
        
        buy_btn = QPushButton("Buy Tickets")
        buy_btn.setFixedHeight(50)
        buy_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        buy_btn.clicked.connect(lambda: self.handle_purchase(content, details_window))
        
        info_layout.addWidget(title)
        info_layout.addWidget(meta)
        info_layout.addSpacing(10)
        info_layout.addWidget(price)
        info_layout.addSpacing(20)
        info_layout.addWidget(plot_title)
        info_layout.addWidget(plot)
        info_layout.addStretch()
        info_layout.addWidget(buy_btn)
        
        layout.addWidget(poster_label)
        layout.addWidget(info_panel)
        
        # Keep reference to prevent GC
        self._details_view = details_window
        details_window.show()

    def handle_purchase(self, content, window):
        reply = QMessageBox.question(window, "Confirm Purchase", 
                                     f"Do you want to buy a ticket for '{content[1]}' for ${content[8]}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.buy_ticket(self.user_data['username'], content[0]):
                QMessageBox.information(window, "Success", "Purchase completed as 'Purchased'!")
                window.close()
            else:
                QMessageBox.critical(window, "Error", "Transaction failed.")
