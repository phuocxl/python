from __future__ import annotations
from app.models.DatabaseConnection import DatabaseConnection


class RegisterMedical:
    def __init__(self,
                 maDangKy=None,
                 tenBenhNhan="",
                 ngaySinh=None,
                 gioiTinh="",
                 diaChi="",
                 sdt="",
                 ngayDangKy=None,
                 trangThai="pending"):
        self.maDangKy = maDangKy
        self.tenBenhNhan = tenBenhNhan
        self.ngaySinh = ngaySinh
        self.gioiTinh = gioiTinh
        self.diaChi = diaChi
        self.sdt = sdt
        self.ngayDangKy = ngayDangKy
        self.trangThai = trangThai

    # -----------------------------------
    # CREATE
    # -----------------------------------
    @staticmethod
    def add_register(data: dict) -> bool:
        """
        Thêm mới lượt đăng ký khám bệnh
        data = {
            "tenBenhNhan": "...",
            "ngaySinh": "...",
            "gioiTinh": "...",
            "diaChi": "...",
            "sdt": "...",
            "ngayDangKy": "...",
            "trangThai": "pending"
        }
        """
        query = """
            INSERT INTO register_medical
            (tenBenhNhan, ngaySinh, gioiTinh, diaChi, sdt, ngayDangKy, trangThai)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["tenBenhNhan"],
            data["ngaySinh"],
            data["gioiTinh"],
            data["diaChi"],
            data["sdt"],
            data["ngayDangKy"],
            data.get("trangThai", "pending")
        )

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, values)
                    conn.commit()
                    print("[INFO] Đăng ký khám thành công!")
                    return True
                except Exception as e:
                    print("[ERROR]", e)
                    return False
                finally:
                    cursor.close()

    # -----------------------------------
    # READ
    # -----------------------------------
    @staticmethod
    def get_all_registers():
        """Lấy toàn bộ danh sách đăng ký khám"""
        query = "SELECT * FROM register_medical ORDER BY ngayDangKy DESC"

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        return []

    @staticmethod
    def get_register_by_id(maDangKy):
        query = "SELECT * FROM register_medical WHERE maDangKy=%s"

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (maDangKy,))
                result = cursor.fetchone()
                cursor.close()
                return result
        return None

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    @staticmethod
    def update_register(maDangKy, data):
        """
        Cập nhật thông tin đăng ký khám
        data có thể giống như add_register
        """
        query = """
            UPDATE register_medical
            SET tenBenhNhan=%s, ngaySinh=%s, gioiTinh=%s,
                diaChi=%s, sdt=%s, ngayDangKy=%s, trangThai=%s
            WHERE maDangKy=%s
        """

        values = (
            data["tenBenhNhan"],
            data["ngaySinh"],
            data["gioiTinh"],
            data["diaChi"],
            data["sdt"],
            data["ngayDangKy"],
            data.get("trangThai", "pending"),
            maDangKy
        )

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, values)
                    conn.commit()
                    return True
                except Exception as e:
                    print("[ERROR]", e)
                    return False
                finally:
                    cursor.close()

    # -----------------------------------
    # DELETE
    # -----------------------------------
    @staticmethod
    def delete_register(maDangKy):
        query = "DELETE FROM register_medical WHERE maDangKy=%s"

        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (maDangKy,))
                    conn.commit()
                    print(f"[INFO] Đã xóa đăng ký {maDangKy}")
                    return True
                except Exception as e:
                    print("[ERROR]", e)
                    return False
                finally:
                    cursor.close()
