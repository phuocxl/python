import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.LoginController import LoginController

# Hàm tiện ích căn giữa
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

class LoginView:
    def __init__(self, parent, on_success=None):
        self.parent = parent
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Đăng nhập hệ thống")
        self.window.resizable(False, False)
        self.window.configure(bg="#f2f2f2")

        window_width = 400
        window_height = 280
        center_window(self.window, window_width, window_height)

        self.create_widgets()
        self.style_widgets()

    # --------------------------------
    def create_widgets(self):
        self.frame = ttk.Frame(self.window, padding=20)
        self.frame.pack(expand=True, fill="both")

        self.title_label = ttk.Label(
            self.frame, text="ĐĂNG NHẬP HỆ THỐNG",
            anchor="center", font=("San Francisco", 16, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        ttk.Label(self.frame, text="Tên đăng nhập:").pack(fill="x")
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.pack(fill="x", pady=(0, 10))

        ttk.Label(self.frame, text="Mật khẩu:").pack(fill="x")
        self.entry_password = ttk.Entry(self.frame, show="*")
        self.entry_password.pack(fill="x", pady=(0, 15))

        self.login_button = ttk.Button(self.frame, text="Đăng nhập", command=self.on_login)
        self.login_button.pack(pady=(10, 0))

    # --------------------------------
    def style_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f2f2f2")
        style.configure("TLabel", background="#f2f2f2", foreground="#333", font=("San Francisco", 12))
        style.configure("TEntry", padding=5)
        style.configure("TButton", background="#4CAF50", foreground="white", font=("San Francisco", 12))
        style.map("TButton", foreground=[("active","white")], background=[("active","#45a049")])

    # --------------------------------
    def on_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        user = LoginController.login(username, password)

        if not user:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            return

        # Đóng Toplevel login trước
        try:
            self.window.destroy()
        except tk.TclError:
            pass  # window đã bị destroy rồi, bỏ qua

        # Gọi callback
        if self.on_success:
            self.on_success(user)
