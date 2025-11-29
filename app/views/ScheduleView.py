# app/views/ScheduleView.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from app.controllers.ScheduleController import ScheduleController
from app.models.DoctorModel import Doctor


class ScheduleView:
    """Trang quản lý lịch làm việc bác sĩ"""

    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.doctors = []

        # Frame chính
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        # Title
        title = ttk.Label(self.frame, text="QUẢN LÝ LỊCH LÀM VIỆC BÁC SĨ",
                          font=("San Francisco", 16, "bold"))
        title.pack(pady=(0, 10))

        self.load_doctors()
        self.create_treeview()
        self.create_form()
        self.create_buttons()
        self.load_schedules()

    def load_doctors(self):
        """Load danh sách bác sĩ"""
        self.doctors = Doctor.get_all_doctors()

    def create_treeview(self):
        """Tạo bảng hiển thị lịch"""
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        columns = ("ma_lich", "ten_bacsi", "ngay_lam_viec", "gio_bat_dau",
                   "gio_ket_thuc", "trang_thai", "ghi_chu")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        headers = ["Mã lịch", "Bác sĩ", "Ngày làm việc", "Giờ bắt đầu",
                   "Giờ kết thúc", "Trạng thái", "Ghi chú"]
        widths = [80, 150, 120, 100, 100, 100, 200]

        for col, text, width in zip(columns, headers, widths):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    def create_form(self):
        """Tạo form nhập liệu"""
        form_frame = ttk.LabelFrame(self.frame, text="Thông tin lịch làm việc", padding=15)
        form_frame.pack(fill="x", padx=10, pady=10)

        # Row 0: Bác sĩ và Ngày làm việc
        ttk.Label(form_frame, text="Bác sĩ:").grid(row=0, column=0, sticky="w", pady=5)
        self.doctor_combo = ttk.Combobox(form_frame, state="readonly", width=25)
        self.doctor_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=(5, 20))

        # Cập nhật danh sách bác sĩ vào combobox
        doctor_names = [f"{d.get('MaDoctorID')} - {d.get('Name')}" for d in self.doctors]
        self.doctor_combo['values'] = doctor_names

        ttk.Label(form_frame, text="Ngày làm việc:").grid(row=0, column=2, sticky="w", pady=5)
        self.date_entry = DateEntry(form_frame, width=20, background='darkblue',
                                    foreground='white', borderwidth=2,
                                    date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=3, sticky="ew", pady=5)

        # Row 1: Giờ bắt đầu và Giờ kết thúc
        ttk.Label(form_frame, text="Giờ bắt đầu:").grid(row=1, column=0, sticky="w", pady=5)
        self.start_time_entry = ttk.Entry(form_frame, width=27)
        self.start_time_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(5, 20))
        self.start_time_entry.insert(0, "08:00:00")

        ttk.Label(form_frame, text="Giờ kết thúc:").grid(row=1, column=2, sticky="w", pady=5)
        self.end_time_entry = ttk.Entry(form_frame, width=22)
        self.end_time_entry.grid(row=1, column=3, sticky="ew", pady=5)
        self.end_time_entry.insert(0, "17:00:00")

        # Row 2: Trạng thái và Ghi chú
        ttk.Label(form_frame, text="Trạng thái:").grid(row=2, column=0, sticky="w", pady=5)
        self.status_combo = ttk.Combobox(form_frame, values=["active", "cancelled", "completed"],
                                         state="readonly", width=25)
        self.status_combo.grid(row=2, column=1, sticky="ew", pady=5, padx=(5, 20))
        self.status_combo.set("active")

        ttk.Label(form_frame, text="Ghi chú:").grid(row=2, column=2, sticky="w", pady=5)
        self.note_entry = ttk.Entry(form_frame, width=22)
        self.note_entry.grid(row=2, column=3, sticky="ew", pady=5)

        # Cấu hình stretch
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

    def create_buttons(self):
        """Tạo các nút chức năng"""
        btn_frame = tk.Frame(self.frame, bg="#f7f7f7", pady=10)
        btn_frame.pack()

        # Nút Thêm - Xanh lá nhạt
        btn_add = tk.Button(btn_frame, text="➕ Thêm lịch", width=15,
                            font=("San Francisco", 10, "bold"),
                            bg="#d5f4e6", fg="black", relief="flat", cursor="hand2",
                            activebackground="#a9dfbf", activeforeground="black",
                            command=self.add_schedule)
        btn_add.grid(row=0, column=0, padx=5)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#a9dfbf"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#d5f4e6"))

        # Nút Cập nhật - Xanh dương nhạt
        btn_update = tk.Button(btn_frame, text="✏️ Cập nhật", width=15,
                               font=("San Francisco", 10, "bold"),
                               bg="#d4e6f1", fg="black", relief="flat", cursor="hand2",
                               activebackground="#aed6f1", activeforeground="black",
                               command=self.update_schedule)
        btn_update.grid(row=0, column=1, padx=5)
        btn_update.bind("<Enter>", lambda e: btn_update.config(bg="#aed6f1"))
        btn_update.bind("<Leave>", lambda e: btn_update.config(bg="#d4e6f1"))

        # Nút Xóa - Đỏ nhạt
        btn_delete = tk.Button(btn_frame, text="🗑️ Xóa", width=15,
                               font=("San Francisco", 10, "bold"),
                               bg="#fadbd8", fg="black", relief="flat", cursor="hand2",
                               activebackground="#f5b7b1", activeforeground="black",
                               command=self.delete_schedule)
        btn_delete.grid(row=0, column=2, padx=5)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#f5b7b1"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg="#fadbd8"))

        # Nút Làm mới - Xám nhạt
        btn_refresh = tk.Button(btn_frame, text="🔄 Làm mới", width=15,
                                font=("San Francisco", 10, "bold"),
                                bg="#e5e7e9", fg="black", relief="flat", cursor="hand2",
                                activebackground="#d5d8dc", activeforeground="black",
                                command=self.load_schedules)
        btn_refresh.grid(row=0, column=3, padx=5)
        btn_refresh.bind("<Enter>", lambda e: btn_refresh.config(bg="#d5d8dc"))
        btn_refresh.bind("<Leave>", lambda e: btn_refresh.config(bg="#e5e7e9"))

    def load_schedules(self):
        """Load danh sách lịch làm việc"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        schedules = ScheduleController.get_all_schedules()
        for s in schedules:
            self.tree.insert("", "end", values=(
                s.get("ma_lich", ""),
                s.get("ten_bacsi", ""),
                s.get("ngay_lam_viec", ""),
                s.get("gio_bat_dau", ""),
                s.get("gio_ket_thuc", ""),
                s.get("trang_thai", ""),
                s.get("ghi_chu", "")
            ))

        self.clear_form()

    def on_select_item(self, event):
        """Xử lý khi chọn item trong tree"""
        item = self.tree.selection()
        if not item:
            return

        data = self.tree.item(item)["values"]
        self.selected_id = data[0]

        # Tìm và set bác sĩ
        doctor_text = data[1]
        for idx, val in enumerate(self.doctor_combo['values']):
            if doctor_text in val:
                self.doctor_combo.current(idx)
                break

        # Set ngày
        try:
            date_obj = datetime.strptime(str(data[2]), "%Y-%m-%d")
            self.date_entry.set_date(date_obj)
        except:
            pass

        # Set giờ
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, str(data[3]))

        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, str(data[4]))

        # Set trạng thái
        self.status_combo.set(data[5])

        # Set ghi chú
        self.note_entry.delete(0, tk.END)
        self.note_entry.insert(0, str(data[6]))

    def get_form_data(self):
        """Lấy dữ liệu từ form"""
        doctor_text = self.doctor_combo.get()
        ma_bacsi = None
        if doctor_text:
            ma_bacsi = int(doctor_text.split(" - ")[0])

        return {
            "ma_bacsi": ma_bacsi,
            "ngay_lam_viec": self.date_entry.get_date().strftime("%Y-%m-%d"),
            "gio_bat_dau": self.start_time_entry.get().strip(),
            "gio_ket_thuc": self.end_time_entry.get().strip(),
            "trang_thai": self.status_combo.get(),
            "ghi_chu": self.note_entry.get().strip()
        }

    def clear_form(self):
        """Xóa form"""
        self.selected_id = None
        self.doctor_combo.set("")
        self.date_entry.set_date(datetime.now())
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, "08:00:00")
        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, "17:00:00")
        self.status_combo.set("active")
        self.note_entry.delete(0, tk.END)

    def validate_form(self, data):
        """Validate dữ liệu form"""
        if not data["ma_bacsi"]:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ")
            return False

        if not data["gio_bat_dau"] or not data["gio_ket_thuc"]:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ giờ làm việc")
            return False

        # Validate format giờ
        try:
            datetime.strptime(data["gio_bat_dau"], "%H:%M:%S")
            datetime.strptime(data["gio_ket_thuc"], "%H:%M:%S")
        except:
            messagebox.showerror("Lỗi", "Định dạng giờ không hợp lệ (HH:MM:SS)")
            return False

        return True

    def add_schedule(self):
        """Thêm lịch làm việc mới"""
        data = self.get_form_data()

        if not self.validate_form(data):
            return

        if ScheduleController.create_schedule(data):
            messagebox.showinfo("Thành công", "Đã thêm lịch làm việc")
            self.load_schedules()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm lịch làm việc")

    def update_schedule(self):
        """Cập nhật lịch làm việc"""
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch cần cập nhật")
            return

        data = self.get_form_data()

        if not self.validate_form(data):
            return

        if ScheduleController.update_schedule(self.selected_id, data):
            messagebox.showinfo("Thành công", "Cập nhật lịch thành công")
            self.load_schedules()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật lịch")

    def delete_schedule(self):
        """Xóa lịch làm việc"""
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch cần xóa")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa lịch này?")
        if not confirm:
            return

        if ScheduleController.delete_schedule(self.selected_id):
            messagebox.showinfo("Thành công", "Đã xóa lịch làm việc")
            self.load_schedules()
        else:
            messagebox.showerror("Lỗi", "Không thể xóa lịch")