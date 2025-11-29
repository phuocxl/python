# app/models/ReportModel.py
from app.models.DatabaseConnection import DatabaseConnection
from datetime import datetime, timedelta


class Report:
    """Model quản lý báo cáo và thống kê"""

    @staticmethod
    def get_monthly_registrations(year=None):
        """Lấy số lượng đăng ký khám theo tháng trong năm"""
        if year is None:
            year = datetime.now().year

        query = """
            SELECT
                MONTH(ngayDangKy) as thang,
                COUNT(*) as so_luong
            FROM register_medical
            WHERE YEAR(ngayDangKy) = %s
            GROUP BY MONTH(ngayDangKy)
            ORDER BY thang
        """

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query, (year,))
                    result = cursor.fetchall()

                    # Tạo dict với 12 tháng, mặc định = 0
                    monthly_data = {i: 0 for i in range(1, 13)}
                    for row in result:
                        monthly_data[row['thang']] = row['so_luong']

                    return monthly_data
                except Exception as e:
                    print(f"[ERROR] Lấy báo cáo tháng: {e}")
                    return {i: 0 for i in range(1, 13)}
                finally:
                    cursor.close()
        return {i: 0 for i in range(1, 13)}

    @staticmethod
    def get_registration_by_status():
        """Thống kê đăng ký theo trạng thái"""
        query = """
            SELECT
                trangThai,
                COUNT(*) as so_luong
            FROM register_medical
            GROUP BY trangThai
        """

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"[ERROR] Thống kê trạng thái: {e}")
                    return []
                finally:
                    cursor.close()
        return []

    @staticmethod
    def get_registration_by_specialty():
        """Thống kê đăng ký theo chuyên khoa"""
        query = """
            SELECT
                chuyenKhoa,
                COUNT(*) as so_luong
            FROM register_medical
            GROUP BY chuyenKhoa
            ORDER BY so_luong DESC
        """

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"[ERROR] Thống kê chuyên khoa: {e}")
                    return []
                finally:
                    cursor.close()
        return []

    @staticmethod
    def get_total_statistics():
        """Lấy tổng số liệu thống kê"""
        queries = {
            'total_registrations': "SELECT COUNT(*) as total FROM register_medical",
            'total_users': "SELECT COUNT(*) as total FROM user",
            'total_doctors': "SELECT COUNT(*) as total FROM doctor",
            'pending_registrations': "SELECT COUNT(*) as total FROM register_medical WHERE trangThai='pending'"
        }

        stats = {}
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    for key, query in queries.items():
                        cursor.execute(query)
                        result = cursor.fetchone()
                        stats[key] = result['total'] if result else 0
                except Exception as e:
                    print(f"[ERROR] Thống kê tổng: {e}")
                finally:
                    cursor.close()

        return stats

    @staticmethod
    def get_doctor_workload():
        """Thống kê số lượng bệnh nhân theo bác sĩ"""
        query = """
            SELECT
                bacSi,
                COUNT(*) as so_benh_nhan
            FROM register_medical
            GROUP BY bacSi
            ORDER BY so_benh_nhan DESC
            LIMIT 10
        """

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(query)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"[ERROR] Thống kê bác sĩ: {e}")
                    return []
                finally:
                    cursor.close()
        return []