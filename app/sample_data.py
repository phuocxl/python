# generate_sample_data.py
"""Script tạo dữ liệu mẫu để test chức năng báo cáo"""

from app.models.DatabaseConnection import DatabaseConnection
from datetime import datetime, timedelta
import random


def generate_sample_registrations():
    """Tạo dữ liệu đăng ký mẫu cho 12 tháng"""

    specialties = [
        "Nội tổng quát",
        "Nhi khoa",
        "Tim mạch",
        "Da liễu",
        "Tai-Mũi-Họng"
    ]

    doctors = {
        "Nội tổng quát": ["BS. Nguyễn Văn An", "BS. Trần Thị Bình", "BS. Lê Minh Quang"],
        "Nhi khoa": ["BS. Võ Mai Anh", "BS. Nguyễn Thanh Bình"],
        "Tim mạch": ["BS. Trần Xuân Hòa", "BS. Đặng Thụy Phương"],
        "Da liễu": ["BS. Phạm Hoài Nam", "BS. Lê Quỳnh Như"],
        "Tai-Mũi-Họng": ["BS. Hồ Văn Khải", "BS. Lý Trọng Đức"]
    }

    statuses = ["pending", "confirmed", "completed", "cancelled"]
    status_weights = [0.2, 0.3, 0.4, 0.1]  # Tỷ lệ mỗi trạng thái

    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ"]
    middle_names = ["Văn", "Thị", "Minh", "Hoàng", "Thanh", "Quốc", "Hữu", "Đức", "Anh", "Thu"]
    last_names = ["An", "Bình", "Cường", "Dung", "Em", "Phương", "Giang", "Hà", "Khoa", "Linh"]

    genders = ["Nam", "Nữ"]

    print("🔄 Đang tạo dữ liệu mẫu...")

    with DatabaseConnection() as conn:
        if not conn:
            print("❌ Không thể kết nối database!")
            return

        cursor = conn.cursor()

        # Xóa dữ liệu cũ (nếu muốn)
        # cursor.execute("DELETE FROM register_medical")
        # conn.commit()
        # print("🗑️ Đã xóa dữ liệu cũ")

        total_records = 0
        current_year = datetime.now().year

        # Tạo dữ liệu cho 12 tháng
        for month in range(1, 13):
            # Số lượng đăng ký mỗi tháng (random từ 5-25)
            num_registrations = random.randint(8, 30)

            for _ in range(num_registrations):
                # Random ngày trong tháng
                day = random.randint(1, 28)
                date = datetime(current_year, month, day)

                # Random thông tin
                specialty = random.choice(specialties)
                doctor = random.choice(doctors[specialty])
                status = random.choices(statuses, weights=status_weights)[0]

                # Tạo tên ngẫu nhiên
                full_name = f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"

                # Tạo ngày sinh (20-70 tuổi)
                age = random.randint(20, 70)
                birth_year = current_year - age
                birth_date = f"{birth_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

                # Tạo SĐT
                phone = f"0{random.randint(300000000, 999999999)}"

                gender = random.choice(genders)

                # Insert vào database
                query = """
                    INSERT INTO register_medical
                    (tenBenhNhan, ngaySinh, gioiTinh, diaChi, sdt, ngayDangKy,
                     chuyenKhoa, bacSi, trangThai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    full_name,
                    birth_date,
                    gender,
                    f"Địa chỉ {random.randint(1, 100)}, TP.HCM",
                    phone,
                    date.strftime("%Y-%m-%d"),
                    specialty,
                    doctor,
                    status
                )

                try:
                    cursor.execute(query, values)
                    total_records += 1
                except Exception as e:
                    print(f"⚠️ Lỗi khi thêm bản ghi: {e}")

            conn.commit()
            print(f"✅ Tháng {month}: Đã tạo {num_registrations} đăng ký")

        cursor.close()
        print(f"\n🎉 Hoàn tất! Đã tạo tổng cộng {total_records} bản ghi mẫu")
        print(f"📊 Dữ liệu được phân bố trong năm {current_year}")


if __name__ == "__main__":
    print("=" * 60)
    print("📝 TẠO DỮ LIỆU MẪU CHO BÁO CÁO")
    print("=" * 60)
    print()

    confirm = input("⚠️ Bạn có chắc muốn tạo dữ liệu mẫu? (y/n): ")

    if confirm.lower() == 'y':
        generate_sample_registrations()
    else:
        print("❌ Đã hủy!")
