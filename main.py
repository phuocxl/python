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
        toolbar = tk.Frame(self.root, bg="#d9d9d9", height=40)
        toolbar.pack(side="top", fill="x")

        btn_home = tk.Button(toolbar, text="Trang chủ", bg="#d9d9d9", fg="black",
                             font=("SF Pro Text", 10, "bold"), relief="flat", padx=10, pady=5,
                             command=self.show_home_page)
        btn_register = tk.Button(toolbar, text="Đăng ký khám bệnh", bg="#d9d9d9", fg="black",
                                 font=("SF Pro Text", 10, "bold"), relief="flat", padx=10, pady=5,
                                 command=self.show_register_page)
        btn_login = tk.Button(toolbar, text="Đăng nhập Admin", bg="#d9d9d9", fg="black",
                              font=("SF Pro Text", 10, "bold"), relief="flat", padx=10, pady=5,
                              command=self.open_login)
        btn_exit = tk.Button(toolbar, text="Thoát", bg="#d9d9d9", fg="black",
                             font=("SF Pro Text", 10, "bold"), relief="flat", padx=10, pady=5,
                             command=self.root.quit)

        for btn in [btn_home, btn_register, btn_login]:
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

        # Sau khi login thành công, đóng MainApp ban đầu
        self.root.destroy()

        # Mở form mới tùy role
        if role == "admin":
            AdminView(tk.Tk(), user)
        elif role == "bacsi":
            tk.messagebox.showinfo("OK", "Bác sĩ đăng nhập thành công!")
        elif role == "letan":
            tk.messagebox.showinfo("OK", "Lễ tân đăng nhập thành công!")
        else:
            tk.messagebox.showinfo("OK", f"Đăng nhập thành công! Role: {role}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
