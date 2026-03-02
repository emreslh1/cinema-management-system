import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseManager:
    def __init__(self, db_name="cinema.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT,
                    role TEXT NOT NULL CHECK(role IN ('Admin', 'User'))
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('Movie', 'TV Series')),
                    genre TEXT,
                    duration TEXT,
                    image_path TEXT,
                    plot TEXT,
                    release_date TEXT,
                    price REAL DEFAULT 10.0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content_id INTEGER,
                    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (content_id) REFERENCES contents(id)
                )
            ''')
            conn.commit()
            
            # Create default admin if not exists
            self.create_user("admin", "admin123", "Admin", "System Admin")
            # Create default user if not exists
            self.create_user("user", "user123", "User", "Default User")

    def create_user(self, username, password, role, full_name=None):
        hashed_pw = generate_password_hash(password)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                    (username, hashed_pw, role, full_name)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_all_users(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, role FROM users")
            return cursor.fetchall()

    def add_content(self, title, c_type, genre, duration, image_path, plot="", release_date="", price=10.0):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contents (title, type, genre, duration, image_path, plot, release_date, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, c_type, genre, duration, image_path, plot, release_date, price)
            )
            conn.commit()

    def get_all_contents(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contents")
            return cursor.fetchall()

    def authenticate_user(self, username, password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result and check_password_hash(result[0], password):
                return {"username": username, "role": result[1]}
        return None

    def delete_content(self, content_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contents WHERE id = ?", (content_id,))
            conn.commit()

    def update_content(self, content_id, title, c_type, genre, duration, image_path, plot="", release_date="", price=10.0):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contents SET title = ?, type = ?, genre = ?, duration = ?, image_path = ?, plot = ?, release_date = ?, price = ? WHERE id = ?",
                (title, c_type, genre, duration, image_path, plot, release_date, price, content_id)
            )
            conn.commit()

    def buy_ticket(self, username, content_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()
            if user_id:
                cursor.execute(
                    "INSERT INTO purchases (user_id, content_id) VALUES (?, ?)",
                    (user_id[0], content_id)
                )
                conn.commit()
                return True
        return False
