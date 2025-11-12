# app/models/DoctorModel.py
from app.models.DatabaseConnection import DatabaseConnection

class Doctor:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    @staticmethod
    def add_doctor(name, username, password):
        """
        Thêm bác sĩ mới vào database
        """
        query = "INSERT INTO doctor (Name, Username, PasswordHash) VALUES (%s, %s, %s)"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (name, username, password))
                    conn.commit()
                    print(f"[INFO] Đã thêm bác sĩ: {name}")
                except Exception as e:
                    print(f"[ERROR] {e}")
                finally:
                    cursor.close()

    @staticmethod
    def get_all_doctors():
        """
        Lấy danh sách tất cả bác sĩ
        """
        query = "SELECT * FROM doctor"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        return []