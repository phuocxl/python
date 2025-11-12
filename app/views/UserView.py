import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.UserController import UserController

class UserView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý User")
        self.window.geometry("750x500")
        self.window.resizable(False, False)
        self.window.configure(bg="#f2f2f2")

        self.selected_user_id = None

        self.create_treeview()
        self.create_form()
        self.create_buttons()
        self.load_users()

    def create_treeview(self):
        """Tạo Treeview hiển thị danh sách user"""
        frame = ttk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        columns = ("MaUser","Username","Email","Role","Status")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        for col, text in zip(columns, ["ID","Username","Email","Role","Trạng thái"]):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=120 if col!="Email" else 200)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_user)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def create_form(self):
        """Tạo form nhập liệu user"""
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Username:").grid(row=0,column=0, sticky="w", pady=2)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0,column=1, sticky="ew", pady=2)

        ttk.Label(frame, text="Password:").grid(row=1,column=0, sticky="w", pady=2)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1,column=1, sticky="ew", pady=2)

        ttk.Label(frame, text="Email:").grid(row=2,column=0, sticky="w", pady=2)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=2,column=1, sticky="ew", pady=2)

        ttk.Label(frame, text="Role:").grid(row=0,column=2, sticky="w", padx=(10,0), pady=2)
        self.role_combo = ttk.Combobox(frame, values=["admin","bacSi","letan"], state="readonly")
        self.role_combo.grid(row=0,column=3, sticky="ew", pady=2)
        self.role_combo.set("admin")

        ttk.Label(frame, text="Trạng thái:").grid(row=1,column=2, sticky="w", padx=(10,0), pady=2)
        self.status_combo = ttk.Combobox(frame, values=["active","inactive"], state="readonly")
        self.status_combo.grid(row=1,column=3, sticky="ew", pady=2)
        self.status_combo.set("active")

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

    def create_buttons(self):
        """Tạo các nút CRUD"""
        frame = ttk.Frame(self.window, padding=10)
        frame.pack()

        ttk.Button(frame, text="Thêm", width=15, command=self.add_user).grid(row=0,column=0,padx=5)
        ttk.Button(frame, text="Cập nhật", width=15, command=self.update_user).grid(row=0,column=1,padx=5)
        ttk.Button(frame, text="Xóa", width=15, command=self.delete_user).grid(row=0,column=2,padx=5)
        ttk.Button(frame, text="Làm mới", width=15, command=self.load_users).grid(row=0,column=3,padx=5)

    # -------------------
    # CRUD Methods
    # -------------------
    def load_users(self):
        """Load tất cả user vào Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = UserController.get_all_users()
        for u in users:
            self.tree.insert("", "end", values=(u["ma_user"], u["username"], u["email"], u["role"], u["status"]))
        self.clear_form()

    def on_select_user(self, event):
        """Hiển thị dữ liệu user khi chọn"""
        item = self.tree.selection()
        if not item:
            return
        user = self.tree.item(item)["values"]
        self.selected_user_id = user[0]
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, user[1])
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, user[2])
        self.role_combo.set(user[3])
        self.status_combo.set(user[4])

    def get_form_data(self):
        """Lấy dữ liệu từ form"""
        return {
            "username": self.username_entry.get().strip(),
            "password": self.password_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "role": self.role_combo.get(),
            "status": self.status_combo.get()
        }

    def clear_form(self):
        """Xóa dữ liệu trên form"""
        self.selected_user_id = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.role_combo.set("admin")
        self.status_combo.set("active")

    def add_user(self):
        data = self.get_form_data()
        if not data["username"] or not data["password"]:
            messagebox.showwarning("Cảnh báo","Username và Password là bắt buộc")
            return
        if UserController.create_user(**data):
            messagebox.showinfo("Thành công","Đã thêm user")
            self.load_users()
        else:
            messagebox.showerror("Lỗi","Không thể thêm user")

    def update_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Cảnh báo","Chọn user cần cập nhật")
            return
        data = self.get_form_data()
        if UserController.update_user(self.selected_user_id, **data):
            messagebox.showinfo("Thành công","Cập nhật user thành công")
            self.load_users()
        else:
            messagebox.showerror("Lỗi","Không thể cập nhật user")

    def delete_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Cảnh báo", "Chọn user cần xóa")
            return
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa user này?")
        if not confirm:
            return
        if UserController.delete_user(self.selected_user_id):
            self.load_users()
