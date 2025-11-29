# init_all_tables.py
"""Script khởi tạo TẤT CẢ các bảng cần thiết"""

from app.models.DatabaseConnection import DatabaseConnection


def create_doctor_table():
    """Tạo bảng doctor"""
    print("\n📋 Tạo bảng doctor...")
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
                print("   ✅ Bảng doctor đã sẵn sàng")
                return True
            except Exception as e:
                print(f"   ❌ Lỗi: {e}")
                return False
            finally:
                cursor.close()
    return False


def create_schedule_table():
    """Tạo bảng schedule"""
    print("\n📋 Tạo bảng schedule...")
    query = """
    CREATE TABLE IF NOT EXISTS schedule (
        ma_lich INT AUTO_INCREMENT PRIMARY KEY,
        ma_bacsi INT NOT NULL,
        ngay_lam_viec DATE NOT NULL,
        gio_bat_dau TIME NOT NULL,
        gio_ket_thuc TIME NOT NULL,
        trang_thai VARCHAR(20) DEFAULT 'active',
        ghi_chu TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_ma_bacsi (ma_bacsi)
    )
    """

    with DatabaseConnection() as conn:
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                conn.commit()
                print("   ✅ Bảng schedule đã sẵn sàng")
                return True
            except Exception as e:
                print(f"   ❌ Lỗi: {e}")
                return False
            finally:
                cursor.close()
    return False


def add_sample_doctors():
    """Thêm bác sĩ mẫu"""
    print("\n👨‍⚕️ Thêm dữ liệu bác sĩ mẫu...")

    with DatabaseConnection() as conn:
        if conn:
            cursor = conn.cursor()
            try:
                # Kiểm tra đã có dữ liệu chưa
                cursor.execute("SELECT COUNT(*) FROM doctor")
                count = cursor.fetchone()[0]

                if count == 0:
                    sample_doctors = [
                        ("BS. Nguyễn Văn An", "bacsi_an", "123456"),
                        ("BS. Trần Thị Bình", "bacsi_binh", "123456"),
                        ("BS. Lê Văn Cường", "bacsi_cuong", "123456"),
                        ("BS. Phạm Thị Dung", "bacsi_dung", "123456")
                    ]

                    query = "INSERT INTO doctor (Name, Username, PasswordHash) VALUES (%s, %s, %s)"
                    cursor.executemany(query, sample_doctors)
                    conn.commit()
                    print(f"   ✅ Đã thêm {len(sample_doctors)} bác sĩ mẫu")
                else:
                    print(f"   ℹ️ Bảng doctor đã có {count} bác sĩ")

            except Exception as e:
                print(f"   ❌ Lỗi: {e}")
            finally:
                cursor.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🏥 KHỞI TẠO DATABASE - HỆ THỐNG QUẢN LÝ PHÒNG KHÁM")
    print("=" * 60)

    # Bước 1: Tạo bảng doctor
    if create_doctor_table():
        # Bước 2: Thêm dữ liệu mẫu
        add_sample_doctors()

    # Bước 3: Tạo bảng schedule
    create_schedule_table()

    print("\n" + "=" * 60)
    print("✅ HOÀN TẤT KHỞI TẠO DATABASE!")
    print("=" * 60)
    print("\n📝 Bạn có thể chạy ứng dụng bằng lệnh: python main.py")