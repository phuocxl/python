import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG


class DatabaseConnection:
    """Quản lý kết nối tới MySQL — hỗ trợ dùng 'with' để tự động đóng."""

    def __init__(self):
        self.connection = None

    def connect(self):
        """Tạo kết nối MySQL."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("✅ Kết nối MySQL thành công!")
        except Error as e:
            print(f"❌ Lỗi kết nối MySQL: {e}")
            self.connection = None
        return self.connection

    def close(self):
        """Đóng kết nối."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Đã đóng kết nối MySQL.")

    def __enter__(self):
        """Cho phép dùng 'with DatabaseConnection() as conn:' """
        self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Tự động đóng kết nối khi ra khỏi khối with."""
        self.close()


# ✅ Hàm tiện ích cũ (giữ lại để tương thích các module khác)
def create_connection():
    db = DatabaseConnection()
    return db.connect()
