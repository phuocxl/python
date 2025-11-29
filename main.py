import tkinter as tk
from tkinter import messagebox
from app.views.AdminView import AdminView
from app.views.LoginView import LoginView
from app.views.RegisterMedicalView import RegisterMedicalView


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ thống phòng khám")
        # self.root.geometry("1200x720")
        self.root.resizable(False, False)
        window_width = 1200
        window_height = 720
        center_window(self.root, window_width, window_height)

        # Toolbar/menu
        self.create_toolbar()

        # Container chính
        self.content_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.content_frame.pack(fill="both", expand=True)

        # Trang chính hiển thị thông báo chào mừng
        self.show_home_page()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#e8e8e8", height=45)
        toolbar.pack(side="top", fill="x")

        # Trang chủ - Xanh dương nhạt
        btn_home = tk.Button(toolbar, text="🏠 Trang chủ", bg="#d4e6f1", fg="black",
                             font=("SF Pro Text", 10, "bold"), relief="flat", padx=15, pady=8,
                             cursor="hand2", activebackground="#aed6f1", activeforeground="black",
                             command=self.show_home_page)
        btn_home.bind("<Enter>", lambda e: btn_home.config(bg="#aed6f1"))
        btn_home.bind("<Leave>", lambda e: btn_home.config(bg="#d4e6f1"))

        # Đăng ký khám - Xanh lá nhạt
        btn_register = tk.Button(toolbar, text="📝 Đăng ký khám bệnh", bg="#d5f4e6", fg="black",
                                 font=("SF Pro Text", 10, "bold"), relief="flat", padx=15, pady=8,
                                 cursor="hand2", activebackground="#a9dfbf", activeforeground="black",
                                 command=self.show_register_page)
        btn_register.bind("<Enter>", lambda e: btn_register.config(bg="#a9dfbf"))
        btn_register.bind("<Leave>", lambda e: btn_register.config(bg="#d5f4e6"))

        # Tra cứu lịch - Cam nhạt
        btn_my_appointment = tk.Button(toolbar, text="🔍 Tra cứu lịch khám", bg="#fdebd0", fg="black",
                                       font=("SF Pro Text", 10, "bold"), relief="flat", padx=15, pady=8,
                                       cursor="hand2", activebackground="#fad7a0", activeforeground="black",
                                       command=self.show_my_appointment_page)
        btn_my_appointment.bind("<Enter>", lambda e: btn_my_appointment.config(bg="#fad7a0"))
        btn_my_appointment.bind("<Leave>", lambda e: btn_my_appointment.config(bg="#fdebd0"))

        # Đăng nhập Admin - Tím nhạt
        btn_login = tk.Button(toolbar, text="👤 Đăng nhập Admin", bg="#e8daef", fg="black",
                              font=("SF Pro Text", 10, "bold"), relief="flat", padx=15, pady=8,
                              cursor="hand2", activebackground="#d2b4de", activeforeground="black",
                              command=self.open_login)
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#d2b4de"))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#e8daef"))

        # Thoát - Đỏ nhạt
        btn_exit = tk.Button(toolbar, text="❌ Thoát", bg="#fadbd8", fg="black",
                             font=("SF Pro Text", 10, "bold"), relief="flat", padx=15, pady=8,
                             cursor="hand2", activebackground="#f5b7b1", activeforeground="black",
                             command=self.root.quit)
        btn_exit.bind("<Enter>", lambda e: btn_exit.config(bg="#f5b7b1"))
        btn_exit.bind("<Leave>", lambda e: btn_exit.config(bg="#fadbd8"))

        for btn in [btn_home, btn_register, btn_my_appointment, btn_login]:
            btn.pack(side="left", padx=5, pady=5)
        btn_exit.pack(side="right", padx=5, pady=5)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home_page(self):
        self.clear_content()
        frame = tk.Frame(self.content_frame, bg="#f7f7f7")
        frame.pack(fill="both", expand=True)
        label = tk.Label(frame, text="Chào mừng đến Hệ thống phòng khám",
                         font=("SF Pro Display", 20), bg="#f7f7f7")
        label.pack(pady=50)

    def show_register_page(self):
        self.clear_content()
        frame = tk.Frame(self.content_frame, bg="#f7f7f7")
        frame.pack(fill="both", expand=True)
        RegisterMedicalView(frame)

    def show_my_appointment_page(self):
        self.clear_content()
        from app.views.MyAppointmentView import MyAppointmentView
        MyAppointmentView(self.content_frame)

    # =====================================================
    # LOGIN PROCESS VỚI ẨN ROOT
    # =====================================================
    # def open_login(self):
    #     # Ẩn root tạm thời
    #     self.root.withdraw()
    #     LoginView(self.root, on_success=self.on_login_success)
    def open_login(self):
        # Ẩn root tạm thời
        self.root.withdraw()
        LoginView(self.root, on_success=self.on_login_success)

    def on_login_success(self, response):
        user = response.get("user", {})
        if not user:
            messagebox.showerror("Lỗi", "Đăng nhập thất bại!")
            self.root.deiconify()  # hiện lại root nếu thất bại
            return

        # Đăng nhập thành công → mở form tiếp theo
        self.handle_user_role(user)

    def handle_user_role(self, user):
        role = (user.get("role") or "").lower()

        # Mở form tùy role
        if role == "admin":
            # Ẩn MainApp thay vì destroy
            self.root.withdraw()
            # Tạo cửa sổ Admin mới
            admin_window = tk.Toplevel(self.root)
            AdminView(admin_window, user, on_exit=self.on_admin_exit)
        elif role == "bacsi":
            tk.messagebox.showinfo("OK", "Bác sĩ đăng nhập thành công!")
            self.root.deiconify()
        elif role == "letan":
            tk.messagebox.showinfo("OK", "Lễ tân đăng nhập thành công!")
            self.root.deiconify()
        else:
            tk.messagebox.showinfo("OK", f"Đăng nhập thành công! Role: {role}")
            self.root.deiconify()

    def on_admin_exit(self):
        """Callback khi thoát khỏi trang Admin"""
        self.root.deiconify()  # Hiện lại MainApp
        self.show_home_page()  # Về trang chủ

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
