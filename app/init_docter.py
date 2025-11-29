# init_doctor_table.py
"""Script khởi tạo bảng doctor trong database"""

from app.models.DatabaseConnection import DatabaseConnection


def create_doctor_table():
    """Tạo bảng doctor"""
    query = """
    CREATE TABLE IF NOT EXISTS doctor (
        MaDoctorID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        Username VARCHAR(50) UNIQUE,
        PasswordHash VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    with DatabaseConnection() as conn:
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                conn.commit()
                print("[INFO] Bảng doctor đã sẵn sàng")
                return True
            except Exception as e:
                print(f"[ERROR] Tạo bảng doctor: {e}")
                return False
            finally:
                cursor.close()
    return False


if __name__ == "__main__":
    print("Đang khởi tạo bảng doctor...")
    if create_doctor_table():
        print("Hoàn tất!")

        # Thêm vài bác sĩ mẫu
        print("\nThêm dữ liệu mẫu...")
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    # Kiểm tra xem đã có dữ liệu chưa
                    cursor.execute("SELECT COUNT(*) FROM doctor")
                    count = cursor.fetchone()[0]

                    if count == 0:
                        sample_doctors = [
                            ("Nguyễn Văn A", "bacsi_a", "123456"),
                            ("Trần Thị B", "bacsi_b", "123456"),
                            ("Lê Văn C", "bacsi_c", "123456")
                        ]

                        query = "INSERT INTO doctor (Name, Username, PasswordHash) VALUES (%s, %s, %s)"
                        cursor.executemany(query, sample_doctors)
                        conn.commit()
                        print(f"✅ Đã thêm {len(sample_doctors)} bác sĩ mẫu")
                    else:
                        print(f"ℹ️ Bảng doctor đã có {count} bác sĩ")

                except Exception as e:
                    print(f"[ERROR] Thêm dữ liệu mẫu: {e}")
                finally:
                    cursor.close()
    else:
        print("❌ Không thể tạo bảng doctor")