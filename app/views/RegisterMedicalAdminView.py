import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.RegisterMedicalController import RegisterMedicalController


class RegisterMedicalAdminView:
    """Trang quản lý đăng ký khám bệnh trong AdminView"""

    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None

        # Danh sách chuyên khoa & bác sĩ
        self.chuyen_khoa_list = [
            "Nội tổng quát",
            "Ngoại tổng quát",
            "Tai - Mũi - Họng",
            "Răng - Hàm - Mặt",
            "Tim mạch",
            "Nhi khoa"
        ]

        self.bac_si_theo_khoa = {
            "Nội tổng quát": ["BS. Nguyễn Văn Minh", "BS. Lê Quốc Hùng"],
            "Ngoại tổng quát": ["BS. Trần Văn Khải", "BS. Phạm Tấn Lộc"],
            "Tai - Mũi - Họng": ["BS. Hồ Thu Trang", "BS. Lê Anh Sơn"],
            "Răng - Hàm - Mặt": ["BS. Nguyễn Hữu Tài", "BS. Trịnh Gia Phúc"],
            "Tim mạch": ["BS. Võ Minh Khang", "BS. Đặng Anh Tú"],
            "Nhi khoa": ["BS. Lê Kim Ngân", "BS. Võ Minh Thư"],
        }

        # Frame chính
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.create_treeview()
        self.create_form()
        self.create_buttons()
        self.load_registers()

    # -------------------------------------------------------------
    # TREEVIEW
    # -------------------------------------------------------------
    def create_treeview(self):
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        columns = (
            "maDangKy", "tenBenhNhan", "ngaySinh",
            "gioiTinh", "diaChi", "sdt", "ngayDangKy",
            "chuyenKhoa", "bacSi", "trangThai"
        )

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        headers = [
            "Mã", "Tên bệnh nhân", "Ngày sinh",
            "Giới tính", "Địa chỉ", "SĐT", "Ngày đăng ký",
            "Chuyên khoa", "Bác sĩ", "Trạng thái"
        ]

        for col, text in zip(columns, headers):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=120)

        self.tree.column("diaChi", width=180)
        self.tree.column("bacSi", width=160)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    # -------------------------------------------------------------
    # FORM
    # -------------------------------------------------------------
    def create_form(self):
        form_frame = ttk.Frame(self.frame, padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Hàng 1
        ttk.Label(form_frame, text="Tên bệnh nhân:").grid(row=0, column=0, sticky="w")
        self.ten_entry = ttk.Entry(form_frame)
        self.ten_entry.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(form_frame, text="Giới tính:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.gioiTinh_combo = ttk.Combobox(form_frame, values=["Nam", "Nữ", "Khác"], state="readonly")
        self.gioiTinh_combo.grid(row=0, column=3, sticky="ew")

        ttk.Label(form_frame, text="Trạng thái:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.trangthai_combo = ttk.Combobox(
            form_frame, values=["pending", "confirmed", "cancelled"], state="readonly"
        )
        self.trangthai_combo.grid(row=0, column=5, sticky="ew")

        # Hàng 2
        ttk.Label(form_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        self.ngaySinh_entry = ttk.Entry(form_frame)
        self.ngaySinh_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="SĐT:").grid(row=1, column=2, sticky="w", padx=(10, 0))
        self.sdt_entry = ttk.Entry(form_frame)
        self.sdt_entry.grid(row=1, column=3, sticky="ew")

        ttk.Label(form_frame, text="Chuyên khoa:").grid(row=1, column=4, sticky="w")
        self.chuyenKhoa_combo = ttk.Combobox(form_frame, values=self.chuyen_khoa_list, state="readonly")
        self.chuyenKhoa_combo.grid(row=1, column=5, sticky="ew")
        self.chuyenKhoa_combo.bind("<<ComboboxSelected>>", self.update_doctor_list)

        # Hàng 3
        ttk.Label(form_frame, text="Địa chỉ:").grid(row=2, column=0, sticky="w")
        self.diaChi_entry = ttk.Entry(form_frame)
        self.diaChi_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(form_frame, text="Ngày đăng ký (YYYY-MM-DD):").grid(row=2, column=2, sticky="w", padx=(10, 0))
        self.ngayDangKy_entry = ttk.Entry(form_frame)
        self.ngayDangKy_entry.grid(row=2, column=3, sticky="ew")

        ttk.Label(form_frame, text="Bác sĩ:").grid(row=2, column=4, sticky="w")
        self.bacSi_combo = ttk.Combobox(form_frame, values=[], state="readonly")
        self.bacSi_combo.grid(row=2, column=5, sticky="ew")

        # Layout
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        form_frame.columnconfigure(5, weight=1)

    def create_buttons(self):
        btn_frame = ttk.Frame(self.frame, padding=10)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Thêm", width=15, command=self.add_register).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cập nhật", width=15, command=self.update_register).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Xóa", width=15, command=self.delete_register).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Làm mới", width=15, command=self.load_registers).grid(row=0, column=3, padx=5)

    # -------------------------------------------------------------
    # AUTO UPDATE DOCTOR LIST
    # -------------------------------------------------------------
    def update_doctor_list(self, event=None):
        khoa = self.chuyenKhoa_combo.get()
        ds_bs = self.bac_si_theo_khoa.get(khoa, [])
        self.bacSi_combo["values"] = ds_bs
        if ds_bs:
            self.bacSi_combo.set(ds_bs[0])

    # -------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------
    def load_registers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        registers = RegisterMedicalController.get_all_registers()

        for r in registers:
            self.tree.insert("", "end", values=(
                r.get("maDangKy"),
                r.get("tenBenhNhan"),
                r.get("ngaySinh"),
                r.get("gioiTinh"),
                r.get("diaChi"),
                r.get("sdt"),
                r.get("ngayDangKy"),
                r.get("chuyenKhoa"),
                r.get("bacSi"),
                r.get("trangThai"),
            ))

        self.clear_form()

    def on_select_item(self, event):
        item = self.tree.selection()
        if not item:
            return

        data = self.tree.item(item)["values"]
        self.selected_id = data[0]

        self.ten_entry.delete(0, tk.END)
        self.ten_entry.insert(0, data[1])

        self.ngaySinh_entry.delete(0, tk.END)
        self.ngaySinh_entry.insert(0, data[2])

        self.gioiTinh_combo.set(data[3])
        self.diaChi_entry.delete(0, tk.END)
        self.diaChi_entry.insert(0, data[4])

        self.sdt_entry.delete(0, tk.END)
        self.sdt_entry.insert(0, data[5])

        self.ngayDangKy_entry.delete(0, tk.END)
        self.ngayDangKy_entry.insert(0, data[6])

        self.chuyenKhoa_combo.set(data[7])
        self.update_doctor_list()
        self.bacSi_combo.set(data[8])

        self.trangthai_combo.set(data[9])

    # -------------------------------------------------------------
    def get_form_data(self):
        return {
            "tenBenhNhan": self.ten_entry.get().strip(),
            "ngaySinh": self.ngaySinh_entry.get().strip(),
            "gioiTinh": self.gioiTinh_combo.get(),
            "diaChi": self.diaChi_entry.get().strip(),
            "sdt": self.sdt_entry.get().strip(),
            "ngayDangKy": self.ngayDangKy_entry.get().strip(),
            "chuyenKhoa": self.chuyenKhoa_combo.get(),
            "bacSi": self.bacSi_combo.get(),
            "trangThai": self.trangthai_combo.get(),
        }

    def clear_form(self):
        self.selected_id = None
        self.ten_entry.delete(0, tk.END)
        self.ngaySinh_entry.delete(0, tk.END)
        self.diaChi_entry.delete(0, tk.END)
        self.sdt_entry.delete(0, tk.END)
        self.ngayDangKy_entry.delete(0, tk.END)
        self.gioiTinh_combo.set("Nam")
        self.chuyenKhoa_combo.set("")
        self.bacSi_combo.set("")
        self.trangthai_combo.set("pending")

    # -------------------------------------------------------------
    def add_register(self):
        data = self.get_form_data()

        if not data["tenBenhNhan"] or not data["ngayDangKy"]:
            messagebox.showwarning("Cảnh báo", "Tên bệnh nhân và ngày đăng ký là bắt buộc")
            return

        if RegisterMedicalController.create_register(data):
            messagebox.showinfo("Thành công", "Đã thêm đăng ký khám")
            self.load_registers()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm đăng ký")

    # -------------------------------------------------------------
    def update_register(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Chọn mục cần cập nhật")
            return

        data = self.get_form_data()

        if RegisterMedicalController.update_register(self.selected_id, data):
            messagebox.showinfo("Thành công", "Cập nhật thành công")
            self.load_registers()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật")

    # -------------------------------------------------------------
    def delete_register(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Chọn mục cần xóa")
            return

        confirm = messagebox.askyesno("Xác nhận", "Xóa lượt đăng ký này?")
        if not confirm:
            return

        if RegisterMedicalController.delete_register(self.selected_id):
            messagebox.showinfo("Thành công", "Đã xóa")
            self.load_registers()
        else:
            messagebox.showerror("Lỗi", "Không thể xóa")
