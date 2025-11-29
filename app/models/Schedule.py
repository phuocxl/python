# app/models/ScheduleModel.py
from app.models.DatabaseConnection import DatabaseConnection


class Schedule:
    """Model quản lý lịch làm việc của bác sĩ"""

    def __init__(self, ma_lich=None, ma_bacsi=None, ngay_lam_viec=None,
                 gio_bat_dau=None, gio_ket_thuc=None, trang_thai="active"):
        self.ma_lich = ma_lich
        self.ma_bacsi = ma_bacsi
        self.ngay_lam_viec = ngay_lam_viec
        self.gio_bat_dau = gio_bat_dau
        self.gio_ket_thuc = gio_ket_thuc
        self.trang_thai = trang_thai

    @staticmethod
    def create_table():
        """Tạo bảng schedule nếu chưa tồn tại"""
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
                    print("[INFO] Bảng schedule đã sẵn sàng")
                except Exception as e:
                    print(f"[ERROR] Tạo bảng schedule: {e}")
                finally:
                    cursor.close()

    @staticmethod
    def add_schedule(ma_bacsi, ngay_lam_viec, gio_bat_dau, gio_ket_thuc, ghi_chu=""):
        """Thêm lịch làm việc mới"""
        query = """
            INSERT INTO schedule (ma_bacsi, ngay_lam_viec, gio_bat_dau, gio_ket_thuc, ghi_chu)
            VALUES (%s, %s, %s, %s, %s)
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (ma_bacsi, ngay_lam_viec, gio_bat_dau, gio_ket_thuc, ghi_chu))
                    conn.commit()
                    print(f"[INFO] Đã thêm lịch làm việc cho bác sĩ {ma_bacsi}")
                    return True
                except Exception as e:
                    print(f"[ERROR] Thêm lịch: {e}")
                    return False
                finally:
                    cursor.close()
        return False

    @staticmethod
    def get_all_schedules():
        """Lấy tất cả lịch làm việc kèm thông tin bác sĩ"""
        query = """
            SELECT s.ma_lich, s.ma_bacsi, d.Name as ten_bacsi,
                   s.ngay_lam_viec, s.gio_bat_dau, s.gio_ket_thuc,
                   s.trang_thai, s.ghi_chu
            FROM schedule s
            JOIN doctor d ON s.ma_bacsi = d.MaDoctorID
            ORDER BY s.ngay_lam_viec DESC, s.gio_bat_dau
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
                except Exception as e:
                    print(f"[ERROR] Lấy danh sách lịch: {e}")
                    return []
                finally:
                    cursor.close()
        return []

    @staticmethod
    def get_schedule_by_doctor(ma_bacsi):
        """Lấy lịch làm việc theo bác sĩ"""
        query = """
            SELECT * FROM schedule
            WHERE ma_bacsi = %s
            ORDER BY ngay_lam_viec DESC, gio_bat_dau
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query, (ma_bacsi,))
                    return cursor.fetchall()
                except Exception as e:
                    print(f"[ERROR] Lấy lịch theo bác sĩ: {e}")
                    return []
                finally:
                    cursor.close()
        return []

    @staticmethod
    def update_schedule(ma_lich, ma_bacsi, ngay_lam_viec, gio_bat_dau, gio_ket_thuc, trang_thai, ghi_chu=""):
        """Cập nhật lịch làm việc"""
        query = """
            UPDATE schedule
            SET ma_bacsi=%s, ngay_lam_viec=%s, gio_bat_dau=%s,
                gio_ket_thuc=%s, trang_thai=%s, ghi_chu=%s
            WHERE ma_lich=%s
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (ma_bacsi, ngay_lam_viec, gio_bat_dau,
                                           gio_ket_thuc, trang_thai, ghi_chu, ma_lich))
                    conn.commit()
                    return True
                except Exception as e:
                    print(f"[ERROR] Cập nhật lịch: {e}")
                    return False
                finally:
                    cursor.close()
        return False

    @staticmethod
    def delete_schedule(ma_lich):
        """Xóa lịch làm việc"""
        query = "DELETE FROM schedule WHERE ma_lich=%s"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (ma_lich,))
                    conn.commit()
                    print(f"[INFO] Đã xóa lịch {ma_lich}")
                    return True
                except Exception as e:
                    print(f"[ERROR] Xóa lịch: {e}")
                    return False
                finally:
                    cursor.close()
        return False

    @staticmethod
    def get_schedule_by_date(ngay_lam_viec):
        """Lấy lịch làm việc theo ngày"""
        query = """
            SELECT s.*, d.Name as ten_bacsi
            FROM schedule s
            JOIN doctor d ON s.ma_bacsi = d.MaDoctorID
            WHERE s.ngay_lam_viec = %s
            ORDER BY s.gio_bat_dau
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query, (ngay_lam_viec,))
                    return cursor.fetchall()
                except Exception as e:
                    print(f"[ERROR] Lấy lịch theo ngày: {e}")
                    return []
                finally:
                    cursor.close()
        return []