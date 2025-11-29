import tkinter as tk

from app.views.RegisterMedicalAdminView import RegisterMedicalAdminView
from app.views.UserView import UserView
from app.views.ScheduleView import ScheduleView


class AdminView:
    """Trang Admin chính với các page nằm trong frame lớn"""

    def __init__(self, parent, user, on_exit=None):
        self.parent = parent
        self.user = user
        self.on_exit_callback = on_exit

        # Nếu parent là root, center root và set size
        if isinstance(parent, tk.Tk) or isinstance(parent, tk.Toplevel):
            window_width = 1200
            window_height = 720
            self.center_window(parent, window_width, window_height)

            # Set title cho window
            parent.title(f"Admin Panel - {user.get('username', 'Admin')}")

            # Xử lý sự kiện đóng cửa sổ
            parent.protocol("WM_DELETE_WINDOW", self.exit_admin)

        # Frame chính Admin
        self.admin_frame = tk.Frame(parent, bg="#f7f7f7")
        self.admin_frame.pack(fill="both", expand=True)

        # Toolbar/nút chức năng Admin
        self.toolbar = tk.Frame(self.admin_frame, bg="#34495e", height=45)
        self.toolbar.pack(side="top", fill="x")

        # Quản lý User - Xanh dương
        self.btn_user = tk.Button(
            self.toolbar, text="👥 Quản lý User", width=20,
            font=("San Francisco", 10, "bold"),
            bg="#d4e6f1", fg="black", relief="flat", cursor="hand2",
            activebackground="#aed6f1", activeforeground="black",
            command=self.show_user_page
        )
        self.btn_user.bind("<Enter>", lambda e: self.btn_user.config(bg="#aed6f1"))
        self.btn_user.bind("<Leave>", lambda e: self.btn_user.config(bg="#d4e6f1"))

        # Quản lý Đăng ký khám - Xanh lá
        self.btn_register = tk.Button(
            self.toolbar, text="📋 Quản lý Đăng ký khám", width=20,
            font=("San Francisco", 10, "bold"),
            bg="#d5f4e6", fg="black", relief="flat", cursor="hand2",
            activebackground="#a9dfbf", activeforeground="black",
            command=self.show_register_page
        )
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.config(bg="#a9dfbf"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.config(bg="#d5f4e6"))

        # Lịch làm việc Bác sĩ - Cam
        self.btn_schedule = tk.Button(
            self.toolbar, text="📅 Lịch làm việc Bác sĩ", width=20,
            font=("San Francisco", 10, "bold"),
            bg="#fdebd0", fg="black", relief="flat", cursor="hand2",
            activebackground="#fad7a0", activeforeground="black",
            command=self.show_schedule_page
        )
        self.btn_schedule.bind("<Enter>", lambda e: self.btn_schedule.config(bg="#fad7a0"))
        self.btn_schedule.bind("<Leave>", lambda e: self.btn_schedule.config(bg="#fdebd0"))

        # Báo cáo - Tím
        self.btn_report = tk.Button(
            self.toolbar, text="📊 Báo cáo thống kê", width=20,
            font=("San Francisco", 10, "bold"),
            bg="#e8daef", fg="black", relief="flat", cursor="hand2",
            activebackground="#d2b4de", activeforeground="black",
            command=self.show_report_page
        )
        self.btn_report.bind("<Enter>", lambda e: self.btn_report.config(bg="#d2b4de"))
        self.btn_report.bind("<Leave>", lambda e: self.btn_report.config(bg="#e8daef"))

        # Thoát - Đỏ nhạt
        self.btn_exit = tk.Button(
            self.toolbar, text="🚪 Đăng xuất", width=20,
            font=("San Francisco", 10, "bold"),
            bg="#fadbd8", fg="black", relief="flat", cursor="hand2",
            activebackground="#f5b7b1", activeforeground="black",
            command=self.exit_admin
        )
        self.btn_exit.bind("<Enter>", lambda e: self.btn_exit.config(bg="#f5b7b1"))
        self.btn_exit.bind("<Leave>", lambda e: self.btn_exit.config(bg="#fadbd8"))

        for btn in [self.btn_user, self.btn_register, self.btn_schedule, self.btn_report]:
            btn.pack(side="left", padx=5, pady=5)
        self.btn_exit.pack(side="right", padx=5, pady=5)

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

    def show_schedule_page(self):
        self.clear_content()
        ScheduleView(self.content_frame)

    def show_report_page(self):
        self.clear_content()
        from app.views.ReportView import ReportView
        ReportView(self.content_frame)

    def exit_admin(self):
        """Thoát khỏi trang Admin và quay về MainApp"""
        # Đóng cửa sổ Admin
        if isinstance(self.parent, tk.Toplevel):
            self.parent.destroy()
        else:
            self.admin_frame.destroy()

        # Gọi callback để hiện lại MainApp
        if self.on_exit_callback:
            self.on_exit_callback()
