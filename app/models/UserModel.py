# app/models/UserModel.py
from __future__ import annotations

import hashlib
from tkinter import messagebox

from app.models.DatabaseConnection import DatabaseConnection


class User:
    def __init__(self, username, password, email=None, role="nhanvien", status="active", maUser=None):
        self.maUser = maUser
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.status = status

    @staticmethod
    def hash_password(password: str) -> str:
        """Băm mật khẩu bằng SHA256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    # -------------------
    # LOGIN
    # -------------------
    @staticmethod
    def check_user(username: str, password: str):
        """
        Kiểm tra user dựa trên username và password.
        Password được hash trước khi so sánh.
        """
        query = "SELECT * FROM user WHERE Username=%s"

        with DatabaseConnection() as conn:
            if not conn:
                return None

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()

            if not user:
                return None

            # Hash password nhập vào
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

            # So sánh với PasswordHash trong DB
            if user.get("password") == password_hash:
                return user

        return None

    # -------------------
    # CREATE
    # -------------------
    @staticmethod
    def add_user(username, password, email=None, role="admin", status="active"):
        hashed = User.hash_password(password)
        query = """
            INSERT INTO user (username, password, email, role, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (username, hashed, email, role, status))
                    conn.commit()
                    print(f"[INFO] Đã thêm user: {username}")
                    return True
                except Exception as e:
                    print(f"[ERROR] {e}")
                    return False
                finally:
                    cursor.close()

    # -------------------
    # READ
    # -------------------
    @staticmethod
    def get_all_users():
        query = "SELECT * FROM user"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        return []

    # -------------------
    # UPDATE
    # -------------------
    @staticmethod
    def update_user(ma_user, username, password, email, role, status):
        hashed = User.hash_password(password)
        query = """
            UPDATE user
            SET username=%s, password=%s, email=%s, role=%s, status=%s
            WHERE MaUser=%s
        """
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (username, hashed, email, role, status, ma_user))
                    conn.commit()
                    return True
                except Exception as e:
                    print(f"[ERROR] {e}")
                    return False
                finally:
                    cursor.close()

    @staticmethod
    def delete_user_db(ma_user: int) -> bool:
        query = "DELETE FROM user WHERE ma_user=%s"
        with DatabaseConnection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query, (ma_user,))
                    conn.commit()
                    print(f"[INFO] Đã xóa user MaUser={ma_user}")
                    return True
                except Exception as e:
                    conn.rollback()
                    print(f"[ERROR] Lỗi khi xóa user: {e}")
                    return False
                finally:
                    cursor.close()
            else:
                print("[ERROR] Không thể kết nối cơ sở dữ liệu")
                return False

    # -------------------
    # DELETE
    # -------------------
    @staticmethod
    def delete_user(ma_user):
        """
        Xóa user đã chọn.
        - Kiểm tra nếu là admin thì không cho xóa
        - Hiển thị thông báo qua messagebox
        """
        user = User.get_user_by_id(ma_user)
        if not user:
            messagebox.showerror("Lỗi", "User không tồn tại")
            return False

        role = (user.get("role") or user.get("Role") or "").lower()
        if role == "admin":
            messagebox.showwarning("Cảnh báo", "Không thể xóa user có quyền Admin")
            return False

        # Thực hiện xóa
        success = User.delete_user_db(ma_user)
        if success:
            messagebox.showinfo("Thành công", "Xóa user thành công")
        else:
            messagebox.showerror("Lỗi", "Không thể xóa user")
        return success

    @staticmethod
    def get_user_by_id(ma_user: int) -> dict | None:
        """Lấy thông tin user theo MaUser"""
        query = "SELECT * FROM user WHERE ma_user=%s"
        with User.connect() as conn:
            if not conn:
                return None
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (ma_user,))
            user = cursor.fetchone()
            cursor.close()
            return user
