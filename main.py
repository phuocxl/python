# main.py
import tkinter as tk
from tkinter import messagebox

from app.views.AdminView import AdminView
from app.views.LoginView import LoginView
# from app.views.DoctorView import DoctorView
# from app.views.ReceptionistView import ReceptionistView

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ thống phòng khám")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.show_login()

    def show_login(self):
        """Hiển thị form login"""
        # Xóa widget cũ
        for widget in self.root.winfo_children():
            widget.destroy()
        # Tạo LoginView và truyền callback
        LoginView(self.root, on_success=self.on_login_success)

    def on_login_success(self, response):
        """
        Callback khi login thành công
        `response` là dict trả về từ LoginController
        """
        user = response.get("user", {}) if isinstance(response, dict) else {}
        if not user:
            messagebox.showerror("Lỗi", response.get("message", "Đăng nhập thất bại"))
            # Giữ form login hiện tại
            return

        # Xóa tất cả widget cũ
        for widget in self.root.winfo_children():
            widget.destroy()

        self.handle_user_role(user)

    def handle_user_role(self, user):
        """Xử lý mở view dựa trên role"""
        role = (user.get("role") or user.get("Role") or "").lower()

        role_actions = {
            "admin": lambda: AdminView(self.root, user),
            "bacsi": lambda: messagebox.showinfo("OK", "Đăng nhập thành công! Role: Bác sĩ"),
            "letan": lambda: messagebox.showinfo("OK", "Đăng nhập thành công! Role: Lễ tân"),
        }

        # Thực hiện action, nếu role không xác định thì vẫn thông báo
        action = role_actions.get(role, lambda: messagebox.showinfo("OK", f"Đăng nhập thành công! Role: {role}"))
        action()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
