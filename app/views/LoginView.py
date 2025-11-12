import tkinter as tk
from tkinter import ttk
from app.controllers.LoginController import LoginController

class LoginView:
    def __init__(self, root, on_success=None):
        self.root = root
        self.on_success = on_success
        self.setup_window()
        self.create_widgets()
        self.style_widgets()

    def setup_window(self):
        window_width = 400
        window_height = 280
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.title("Đăng nhập hệ thống")
        self.root.resizable(False, False)
        self.root.configure(bg="#f2f2f2")

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True, fill="both")

        # Title
        self.title_label = ttk.Label(
            self.frame,
            text="ĐĂNG NHẬP HỆ THỐNG",
            anchor="center",
            font=("San Francisco", 16, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        # Username
        self.username_label = ttk.Label(self.frame, text="Tên đăng nhập:", anchor="w")
        self.username_label.pack(fill="x", pady=(0, 5))
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.pack(fill="x", pady=(0, 10))

        # Password
        self.password_label = ttk.Label(self.frame, text="Mật khẩu:", anchor="w")
        self.password_label.pack(fill="x", pady=(0, 5))
        self.entry_password = ttk.Entry(self.frame, show="*")
        self.entry_password.pack(fill="x", pady=(0, 15))

        # Login button
        self.login_button = ttk.Button(self.frame, text="Đăng nhập", command=self.on_login)
        self.login_button.pack(pady=(10, 0))

    def style_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f2f2f2")
        style.configure("TLabel", background="#f2f2f2", foreground="#333", font=("San Francisco", 12))
        style.configure("TEntry", padding=5)
        style.configure("TButton", background="#4CAF50", foreground="white", font=("San Francisco", 12))
        style.map("TButton",
                  foreground=[('active', 'white')],
                  background=[('active', '#45a049')])

    def on_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = LoginController.login(username, password)
        if not user:
            tk.messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            return

        if self.on_success:
            self.on_success(user)


def show_login_view(root, on_success=None):
    LoginView(root, on_success)
