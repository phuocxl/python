# app/views/MyAppointmentView.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.RegisterMedical import RegisterMedical


class MyAppointmentView:
    """Trang tra cứu lịch đăng ký khám của người dùng"""

    def __init__(self, parent):
        self.parent = parent
        self.appointments = []

        # Frame chính
        self.frame = tk.Frame(self.parent, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        self.create_search_section()
        self.create_result_section()

    def create_search_section(self):
        """Tạo phần tìm kiếm"""
        search_frame = tk.Frame(self.frame, bg="white", padx=30, pady=20)
        search_frame.pack(fill="x", padx=20, pady=20)

        # Title
        title = tk.Label(
            search_frame,
            text="TRA CỨU LỊCH ĐĂNG KÝ KHÁM",
            font=("San Francisco", 18, "bold"),
            bg="white",
            fg="#333"
        )
        title.pack(pady=(0, 20))

        # Hướng dẫn
        instruction = tk.Label(
            search_frame,
            text="Nhập số điện thoại để tra cứu lịch đăng ký khám của bạn",
            font=("San Francisco", 11),
            bg="white",
            fg="#666"
        )
        instruction.pack(pady=(0, 15))

        # Input frame
        input_frame = tk.Frame(search_frame, bg="white")
        input_frame.pack()

        tk.Label(
            input_frame,
            text="Số điện thoại:",
            font=("San Francisco", 12),
            bg="white"
        ).pack(side="left", padx=(0, 10))

        self.phone_entry = tk.Entry(
            input_frame,
            font=("San Francisco", 12),
            width=20,
            relief="solid",
            borderwidth=1
        )
        self.phone_entry.pack(side="left", padx=(0, 10))
        self.phone_entry.bind("<Return>", lambda e: self.search_appointments())

        search_btn = tk.Button(
            input_frame,
            text="🔍 Tra cứu",
            font=("San Francisco", 12, "bold"),
            bg="#d4e6f1",
            fg="black",
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2",
            activebackground="#aed6f1",
            activeforeground="black",
            command=self.search_appointments
        )
        search_btn.pack(side="left")

        # Hover effect
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#aed6f1"))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#d4e6f1"))

    def create_result_section(self):
        """Tạo phần hiển thị kết quả"""
        result_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Label kết quả
        self.result_label = tk.Label(
            result_frame,
            text="",
            font=("San Francisco", 12),
            bg="white",
            fg="#333"
        )
        self.result_label.pack(pady=(0, 10))

        # Treeview
        tree_container = tk.Frame(result_frame, bg="white")
        tree_container.pack(fill="both", expand=True)

        columns = ("ma", "ten", "ngay_sinh", "gioi_tinh", "chuyen_khoa",
                   "bac_si", "ngay_kham", "trang_thai")

        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            height=12
        )

        headers = {
            "ma": "Mã ĐK",
            "ten": "Tên bệnh nhân",
            "ngay_sinh": "Ngày sinh",
            "gioi_tinh": "Giới tính",
            "chuyen_khoa": "Chuyên khoa",
            "bac_si": "Bác sĩ",
            "ngay_kham": "Ngày khám",
            "trang_thai": "Trạng thái"
        }

        widths = {
            "ma": 70,
            "ten": 150,
            "ngay_sinh": 100,
            "gioi_tinh": 80,
            "chuyen_khoa": 120,
            "bac_si": 150,
            "ngay_kham": 100,
            "trang_thai": 100
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Style cho trạng thái
        self.tree.tag_configure("pending", background="#fff3cd")
        self.tree.tag_configure("confirmed", background="#d4edda")
        self.tree.tag_configure("completed", background="#d1ecf1")
        self.tree.tag_configure("cancelled", background="#f8d7da")

        # Nút hủy đăng ký
        button_frame = tk.Frame(result_frame, bg="white")
        button_frame.pack(pady=(10, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="❌ Hủy đăng ký đã chọn",
            font=("San Francisco", 11, "bold"),
            bg="#fadbd8",
            fg="black",
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2",
            activebackground="#f5b7b1",
            activeforeground="black",
            command=self.cancel_appointment
        )
        cancel_btn.pack(side="left", padx=5)

        # Hover effect cho cancel button
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#f5b7b1"))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#fadbd8"))

        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Làm mới",
            font=("San Francisco", 11, "bold"),
            bg="#d5f4e6",
            fg="black",
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2",
            activebackground="#a9dfbf",
            activeforeground="black",
            command=self.refresh_results
        )
        refresh_btn.pack(side="left", padx=5)

        # Hover effect cho refresh button
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg="#a9dfbf"))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg="#d5f4e6"))

    def search_appointments(self):
        """Tìm kiếm lịch đăng ký theo số điện thoại"""
        phone = self.phone_entry.get().strip()

        if not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại")
            return

        # Xóa kết quả cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tìm kiếm
        self.appointments = RegisterMedical.get_by_phone(phone)

        if not self.appointments:
            self.result_label.config(
                text=f"❌ Không tìm thấy lịch đăng ký nào với số điện thoại: {phone}",
                fg="#dc3545"
            )
            return

        # Hiển thị kết quả
        self.result_label.config(
            text=f"✅ Tìm thấy {len(self.appointments)} lịch đăng ký",
            fg="#28a745"
        )

        for apt in self.appointments:
            status = apt.get("trangThai", "pending")
            tag = status.lower()

            # Định dạng trạng thái
            status_text = {
                "pending": "Chờ xác nhận",
                "confirmed": "Đã xác nhận",
                "completed": "Đã khám",
                "cancelled": "Đã hủy"
            }.get(status, status)

            self.tree.insert("", "end", values=(
                apt.get("maDangKy", ""),
                apt.get("tenBenhNhan", ""),
                apt.get("ngaySinh", ""),
                apt.get("gioiTinh", ""),
                apt.get("chuyenKhoa", ""),
                apt.get("bacSi", ""),
                apt.get("ngayDangKy", ""),
                status_text
            ), tags=(tag,))

    def cancel_appointment(self):
        """Hủy lịch đăng ký đã chọn"""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch cần hủy")
            return

        item = self.tree.item(selected[0])
        ma_dangky = item["values"][0]
        ten_benhnhan = item["values"][1]
        trang_thai = item["values"][7]

        # Kiểm tra trạng thái
        if trang_thai == "Đã hủy":
            messagebox.showinfo("Thông báo", "Lịch này đã được hủy trước đó")
            return

        if trang_thai == "Đã khám":
            messagebox.showwarning("Cảnh báo", "Không thể hủy lịch đã hoàn thành")
            return

        # Xác nhận
        confirm = messagebox.askyesno(
            "Xác nhận hủy",
            f"Bạn có chắc muốn hủy lịch đăng ký của:\n{ten_benhnhan}?"
        )

        if not confirm:
            return

        # Cập nhật trạng thái
        success = RegisterMedical.update_status(ma_dangky, "cancelled")

        if success:
            messagebox.showinfo("Thành công", "Đã hủy lịch đăng ký")
            self.refresh_results()
        else:
            messagebox.showerror("Lỗi", "Không thể hủy lịch đăng ký")

    def refresh_results(self):
        """Làm mới kết quả tìm kiếm"""
        phone = self.phone_entry.get().strip()
        if phone:
            self.search_appointments()