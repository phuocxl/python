import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.UserController import UserController

class UserView:
    """Trang quản lý User, nhúng trong form chính (AdminView)"""
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None

        # Frame chính của UserView
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.create_treeview()
        self.create_form()
        self.create_buttons()
        self.load_users()

    # -------------------------------
    def create_treeview(self):
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        columns = ("user_id", "username", "role", "email")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        headers = ["ID", "Tên đăng nhập", "Role", "Email"]
        for col, text in zip(columns, headers):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    # -------------------------------
    def create_form(self):
        form_frame = ttk.Frame(self.frame, padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Tên đăng nhập
        ttk.Label(form_frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=2)

        # Password
        ttk.Label(form_frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Role
        ttk.Label(form_frame, text="Role:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.role_combo = ttk.Combobox(form_frame, values=["admin", "bacsi", "letan"], state="readonly")
        self.role_combo.grid(row=0, column=3, sticky="ew")
        self.role_combo.set("admin")

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=1, column=2, sticky="w", padx=(10, 0))
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, sticky="ew", pady=2)

        # Cấu hình stretch
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

    # -------------------------------
    def create_buttons(self):
        btn_frame = ttk.Frame(self.frame, padding=10)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Thêm", width=15, command=self.add_user).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cập nhật", width=15, command=self.update_user).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Xóa", width=15, command=self.delete_user).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Làm mới", width=15, command=self.load_users).grid(row=0, column=3, padx=5)

    # -------------------------------
    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = UserController.get_all_users()  # list dict
        for u in users:
            self.tree.insert("", "end", values=(
                u.get("ma_user") or u.get("user_id"),  # fix key
                u.get("username", ""),
                u.get("role", ""),
                u.get("email", "")
            ))

        self.clear_form()

    # -------------------------------
    def on_select_item(self, event):
        item = self.tree.selection()
        if not item:
            return

        data = self.tree.item(item)["values"]
        self.selected_id = data[0]

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, data[1])
        self.role_combo.set(data[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, data[3])

    # -------------------------------
    def get_form_data(self):
        return {
            "username": self.username_entry.get().strip(),
            "role": self.role_combo.get(),
            "email": self.email_entry.get().strip(),
            "password": self.password_entry.get()
        }

    def clear_form(self):
        self.selected_id = None
        self.username_entry.delete(0, tk.END)
        self.role_combo.set("letan")
        self.email_entry.delete(0, tk.END)

    # -------------------------------
    def add_user(self):
        data = self.get_form_data()
        if not data["username"]:
            messagebox.showwarning("Cảnh báo", "Tên đăng nhập là bắt buộc")
            return
        if UserController.create_user(data):
            messagebox.showinfo("Thành công", "Đã thêm user")
            self.load_users()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm user")

    def update_user(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Chọn user cần cập nhật")
            return
        data = self.get_form_data()
        if UserController.update_user(self.selected_id, data):
            messagebox.showinfo("Thành công", "Cập nhật thành công")
            self.load_users()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật")

    def delete_user(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Chọn user cần xóa")
            return
        confirm = messagebox.askyesno("Xác nhận", "Xóa user này?")
        if not confirm:
            return
        if UserController.delete_user(self.selected_id):
            messagebox.showinfo("Thành công", "Đã xóa")
            self.load_users()
        else:
            messagebox.showerror("Lỗi", "Không thể xóa user")
