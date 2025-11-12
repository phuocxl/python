# app/models/ReceptionistModel.py
from app.models.DatabaseConnection import DatabaseConnection

class Receptionist:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    @staticmethod
    def add_receptionist(name, username, password):
        """
        Thêm nhân viên lễ tân mới vào database
        """
        query = "INSERT INTO receptionist (Name, Username, PasswordHash) VALUES (%s, %s, %s)"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (name, username, password))
                    conn.commit()
                    print(f"[INFO] Đã thêm lễ tân: {name}")
                except Exception as e:
                    print(f"[ERROR] {e}")
                finally:
                    cursor.close()

    @staticmethod
    def get_all_receptionists():
        """
        Lấy danh sách tất cả nhân viên lễ tân
        """
        query = "SELECT * FROM receptionist"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        return []