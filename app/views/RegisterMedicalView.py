import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.RegisterMedicalController import RegisterMedicalController


class RegisterMedicalView:
    """Form đăng ký khám bệnh (có thể nhúng trong frame khác hoặc chạy độc lập)"""

    def __init__(self, parent, standalone=False):
        """
        parent: tk.Frame hoặc tk.Tk
        standalone: nếu True -> tạo cửa sổ Tk độc lập
        """
        if standalone:
            self.window = tk.Tk()
            self.window.title("Đăng ký khám bệnh")
            self.window.geometry("1200x900")
            self.window.resizable(False, False)
            parent = self.window  # vẽ vào window
        else:
            self.window = parent  # nhúng vào frame parent

        self.setup_styles()
        self.build_form(parent)

        if standalone:
            self.window.mainloop()

    # -------------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("MacEntry.TEntry", padding=6, relief="flat", borderwidth=1,
                        foreground="#333", fieldbackground="#fff", bordercolor="#c9c9c9")
        style.map("MacEntry.TEntry", bordercolor=[("focus", "#007aff")])

        style.configure("MacCombo.TCombobox", padding=6, relief="flat", bordercolor="#c9c9c9",
                        arrowsize=17, fieldbackground="white")
        style.map("MacCombo.TCombobox", bordercolor=[("focus", "#007aff")])

        style.configure("MacButton.TButton", background="#007aff", foreground="white",
                        padding=8, relief="flat", font=("SF Pro Text", 12),
                        borderwidth=0, focusthickness=3, focuscolor="#0051a8")
        style.map("MacButton.TButton", background=[("active", "#005fcc")])

    # -------------------------------------------------------------
    def build_form(self, parent):
        container = tk.Frame(parent, bg="white", bd=0, highlightthickness=0)
        container.place(relx=0.5, rely=0.5, anchor="center", width=460, height=450)

        title = tk.Label(container, text="Đăng ký khám bệnh",
                         font=("SF Pro Display", 20, "bold"),
                         bg="white", fg="#222")
        title.pack(pady=18)

        form = ttk.Frame(container)
        form.pack(pady=10, padx=20, fill="x")

        # --- Họ tên ---
        ttk.Label(form, text="Tên bệnh nhân:", font=("SF Pro Text", 12)).grid(row=0, column=0, sticky="w")
        self.ten_entry = ttk.Entry(form, width=30, style="MacEntry.TEntry")
        self.ten_entry.grid(row=0, column=1, pady=6, sticky="ew")

        # --- Ngày sinh ---
        ttk.Label(form, text="Ngày sinh (YYYY-MM-DD):", font=("SF Pro Text", 12)).grid(row=1, column=0, sticky="w")
        self.ngaySinh_entry = ttk.Entry(form, style="MacEntry.TEntry")
        self.ngaySinh_entry.grid(row=1, column=1, pady=6, sticky="ew")

        # --- Giới tính ---
        ttk.Label(form, text="Giới tính:", font=("SF Pro Text", 12)).grid(row=2, column=0, sticky="w")
        self.gioiTinh_combo = ttk.Combobox(form, values=["Nam", "Nữ", "Khác"], state="readonly",
                                           width=27, style="MacCombo.TCombobox")
        self.gioiTinh_combo.grid(row=2, column=1, pady=6, sticky="ew")
        self.gioiTinh_combo.set("Nam")

        # --- Địa chỉ ---
        ttk.Label(form, text="Địa chỉ:", font=("SF Pro Text", 12)).grid(row=3, column=0, sticky="w")
        self.diaChi_entry = ttk.Entry(form, style="MacEntry.TEntry")
        self.diaChi_entry.grid(row=3, column=1, pady=6, sticky="ew")

        # --- SĐT ---
        ttk.Label(form, text="Số điện thoại:", font=("SF Pro Text", 12)).grid(row=4, column=0, sticky="w")
        self.sdt_entry = ttk.Entry(form, style="MacEntry.TEntry")
        self.sdt_entry.grid(row=4, column=1, pady=6, sticky="ew")

        # --- Ngày đăng ký ---
        ttk.Label(form, text="Ngày đăng ký (YYYY-MM-DD):", font=("SF Pro Text", 12)).grid(row=5, column=0, sticky="w")
        self.ngayDangKy_entry = ttk.Entry(form, style="MacEntry.TEntry")
        self.ngayDangKy_entry.grid(row=5, column=1, pady=6, sticky="ew")

        # --- Button ---
        btn = ttk.Button(container, text="Đăng ký khám bệnh", style="MacButton.TButton",
                         command=self.submit_register)
        btn.pack(pady=18)

        form.columnconfigure(1, weight=1)

    # -------------------------------------------------------------
    def submit_register(self):
        data = {
            "tenBenhNhan": self.ten_entry.get().strip(),
            "ngaySinh": self.ngaySinh_entry.get().strip(),
            "gioiTinh": self.gioiTinh_combo.get(),
            "diaChi": self.diaChi_entry.get().strip(),
            "sdt": self.sdt_entry.get().strip(),
            "ngayDangKy": self.ngayDangKy_entry.get().strip(),
            "trangThai": "pending"
        }

        if not data["tenBenhNhan"] or not data["ngayDangKy"]:
            messagebox.showwarning("Thiếu thông tin", "Tên bệnh nhân và ngày đăng ký là bắt buộc.")
            return

        success = RegisterMedicalController.create_register(data)

        if success:
            messagebox.showinfo("Thành công", "Đăng ký khám bệnh thành công!")
            self.clear_form()
        else:
            messagebox.showerror("Lỗi", "Không thể gửi đăng ký. Vui lòng thử lại.")

    # -------------------------------------------------------------
    def clear_form(self):
        self.ten_entry.delete(0, tk.END)
        self.ngaySinh_entry.delete(0, tk.END)
        self.diaChi_entry.delete(0, tk.END)
        self.sdt_entry.delete(0, tk.END)
        self.ngayDangKy_entry.delete(0, tk.END)
        self.gioiTinh_combo.set("Nam")
