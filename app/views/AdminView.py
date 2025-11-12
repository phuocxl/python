from tkinter import ttk

from app.views.UserView import UserView


class AdminView:
    def __init__(self, parent, user):
        """
        parent: tk.Tk hoặc tk.Frame
        user: dict chứa thông tin user hiện tại
        """
        self.parent = parent
        self.user = user

        self.main_frame = ttk.Frame(parent, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        """Xây dựng giao diện admin"""
        # Title
        welcome_label = ttk.Label(self.main_frame, text=f"Xin chào {self.user.get('username', '')}",
                                  font=("San Francisco", 16, "bold"))
        welcome_label.pack(pady=(0, 15))

        subtitle_label = ttk.Label(self.main_frame, text="Chọn chức năng:",
                                   font=("San Francisco", 13))
        subtitle_label.pack(pady=(0, 10))

        # Button frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        # Quản lý User
        ttk.Button(btn_frame, text="Quản lý User", width=25, command=self.open_user_view).pack(pady=5)

        # TODO: Thêm các chức năng khác, ví dụ quản lý Bác sĩ, Lễ tân, Kế toán...
        # ttk.Button(btn_frame, text="Quản lý Bác sĩ", width=25, command=self.open_doctor_view).pack(pady=5)
        # ttk.Button(btn_frame, text="Quản lý Lễ tân", width=25, command=self.open_reception_view).pack(pady=5)

    def open_user_view(self):
        """Mở UserView mà không destroy parent"""
        self.main_frame.destroy()
        UserView(self.parent)
