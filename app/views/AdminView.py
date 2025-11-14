import tkinter as tk

from app.views.RegisterMedicalAdminView import RegisterMedicalAdminView
from app.views.UserView import UserView


class AdminView:
    """Trang Admin chính với các page nằm trong frame lớn"""
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

        # Nếu parent là root, center root và set size
        if isinstance(parent, tk.Tk) or isinstance(parent, tk.Toplevel):
            window_width = 1200
            window_height = 720
            self.center_window(parent, window_width, window_height)

        # Frame chính Admin
        self.admin_frame = tk.Frame(parent, bg="#f7f7f7")
        self.admin_frame.pack(fill="both", expand=True)

        # Toolbar/nút chức năng Admin
        self.toolbar = tk.Frame(self.admin_frame, bg="#d9d9d9", height=40)
        self.toolbar.pack(side="top", fill="x")

        self.btn_user = tk.Button(
            self.toolbar, text="Quản lý User", width=20,
            command=self.show_user_page
        )
        self.btn_register = tk.Button(
            self.toolbar, text="Quản lý Đăng ký khám", width=20,
            command=self.show_register_page
        )
        self.btn_exit = tk.Button(
            self.toolbar, text="Thoát", width=20,
            command=self.exit_admin
        )

        for btn in [self.btn_user, self.btn_register, self.btn_exit]:
            btn.pack(side="left", padx=5, pady=5)

        # Frame hiển thị nội dung page
        self.content_frame = tk.Frame(self.admin_frame, bg="#f7f7f7")
        self.content_frame.pack(fill="both", expand=True)

        # Trang mặc định (chào mừng)
        self.show_home_page()

    # -------------------------------
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home_page(self):
        self.clear_content()
        label = tk.Label(
            self.content_frame, text=f"Xin chào {self.user.get('username', '')}!\nChọn chức năng ở trên.",
            font=("San Francisco", 18), bg="#f7f7f7"
        )
        label.pack(expand=True)

    def show_user_page(self):
        self.clear_content()
        UserView(self.content_frame)

    def show_register_page(self):
        self.clear_content()
        RegisterMedicalAdminView(self.content_frame)

    def exit_admin(self):
        self.admin_frame.destroy()
