# app/views/ReportView.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.models.Report import Report


class ReportView:
    """Trang xem báo cáo và thống kê"""

    def __init__(self, parent):
        self.parent = parent
        self.current_year = datetime.now().year

        # Frame chính
        self.frame = tk.Frame(self.parent, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        # Title
        title_frame = tk.Frame(self.frame, bg="white", pady=15)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        title = tk.Label(
            title_frame,
            text="📊 BÁO CÁO THỐNG KÊ HỆ THỐNG",
            font=("San Francisco", 18, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        title.pack()

        # Container cho nội dung
        content_container = tk.Frame(self.frame, bg="#f7f7f7")
        content_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Tạo các phần
        self.create_summary_cards(content_container)
        self.create_chart_section(content_container)
        self.create_statistics_section(content_container)

    def create_summary_cards(self, parent):
        """Tạo các thẻ tóm tắt thống kê"""
        cards_frame = tk.Frame(parent, bg="#f7f7f7")
        cards_frame.pack(fill="x", pady=(0, 10))

        # Lấy dữ liệu
        stats = Report.get_total_statistics()

        cards_data = [
            ("📋", "Tổng đăng ký", stats.get('total_registrations', 0), "#d4e6f1"),
            ("👥", "Tổng người dùng", stats.get('total_users', 0), "#d5f4e6"),
            ("👨‍⚕️", "Tổng bác sĩ", stats.get('total_doctors', 0), "#fdebd0"),
            ("⏳", "Chờ xác nhận", stats.get('pending_registrations', 0), "#fadbd8")
        ]

        for icon, label, value, color in cards_data:
            self.create_card(cards_frame, icon, label, value, color)

    def create_card(self, parent, icon, label, value, bg_color):
        """Tạo một thẻ thống kê"""
        card = tk.Frame(parent, bg=bg_color, relief="flat", bd=0)
        card.pack(side="left", fill="both", expand=True, padx=5)

        # Icon
        icon_label = tk.Label(
            card,
            text=icon,
            font=("San Francisco", 30),
            bg=bg_color
        )
        icon_label.pack(pady=(15, 5))

        # Value
        value_label = tk.Label(
            card,
            text=str(value),
            font=("San Francisco", 24, "bold"),
            bg=bg_color,
            fg="#2c3e50"
        )
        value_label.pack()

        # Label
        text_label = tk.Label(
            card,
            text=label,
            font=("San Francisco", 11),
            bg=bg_color,
            fg="#555"
        )
        text_label.pack(pady=(5, 15))

    def create_chart_section(self, parent):
        """Tạo phần biểu đồ"""
        chart_frame = tk.Frame(parent, bg="white", relief="flat")
        chart_frame.pack(fill="both", expand=True, pady=10)

        # Header với chọn năm
        header = tk.Frame(chart_frame, bg="white", pady=10)
        header.pack(fill="x", padx=15)

        tk.Label(
            header,
            text="📈 Biểu đồ đăng ký khám theo tháng",
            font=("San Francisco", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side="left")

        # Chọn năm
        year_frame = tk.Frame(header, bg="white")
        year_frame.pack(side="right")

        tk.Label(year_frame, text="Năm:", bg="white", font=("San Francisco", 11)).pack(side="left", padx=(0, 5))

        years = list(range(2020, datetime.now().year + 2))
        self.year_combo = ttk.Combobox(year_frame, values=years, state="readonly", width=8)
        self.year_combo.set(self.current_year)
        self.year_combo.pack(side="left", padx=(0, 10))
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        refresh_btn = tk.Button(
            year_frame,
            text="🔄 Làm mới",
            font=("San Francisco", 10, "bold"),
            bg="#d4e6f1",
            fg="black",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.update_chart
        )
        refresh_btn.pack(side="left")

        # Canvas cho biểu đồ
        self.chart_container = tk.Frame(chart_frame, bg="white")
        self.chart_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.draw_chart()

    def draw_chart(self):
        """Vẽ biểu đồ"""
        # Xóa biểu đồ cũ
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Lấy dữ liệu
        year = int(self.year_combo.get())
        monthly_data = Report.get_monthly_registrations(year)

        # Tạo figure
        fig = Figure(figsize=(10, 4), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)

        # Dữ liệu
        months = list(range(1, 13))
        values = [monthly_data[m] for m in months]
        month_names = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']

        # Vẽ biểu đồ cột
        bars = ax.bar(month_names, values, color='#3498db', alpha=0.8, edgecolor='#2980b9', linewidth=1.5)

        # Thêm giá trị lên đầu cột
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Tùy chỉnh
        ax.set_xlabel('Tháng', fontsize=11, fontweight='bold')
        ax.set_ylabel('Số lượng đăng ký', fontsize=11, fontweight='bold')
        ax.set_title(f'Thống kê đăng ký khám năm {year}', fontsize=13, fontweight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Đặt y-axis bắt đầu từ 0
        ax.set_ylim(bottom=0)

        fig.tight_layout()

        # Nhúng vào Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_chart(self):
        """Cập nhật biểu đồ"""
        self.draw_chart()

    def create_statistics_section(self, parent):
        """Tạo phần thống kê chi tiết"""
        stats_frame = tk.Frame(parent, bg="#f7f7f7")
        stats_frame.pack(fill="both", expand=True, pady=10)

        # Thống kê theo chuyên khoa
        specialty_frame = tk.Frame(stats_frame, bg="white", relief="flat")
        specialty_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(
            specialty_frame,
            text="🏥 Thống kê theo chuyên khoa",
            font=("San Francisco", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            pady=10
        ).pack()

        specialty_tree = ttk.Treeview(specialty_frame, columns=("specialty", "count"),
                                      show="headings", height=8)
        specialty_tree.heading("specialty", text="Chuyên khoa")
        specialty_tree.heading("count", text="Số lượng")
        specialty_tree.column("specialty", width=200, anchor="w")
        specialty_tree.column("count", width=100, anchor="center")

        specialty_data = Report.get_registration_by_specialty()
        for item in specialty_data:
            specialty_tree.insert("", "end", values=(
                item.get('chuyenKhoa', 'N/A'),
                item.get('so_luong', 0)
            ))

        specialty_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Thống kê theo bác sĩ
        doctor_frame = tk.Frame(stats_frame, bg="white", relief="flat")
        doctor_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        tk.Label(
            doctor_frame,
            text="👨‍⚕️ Top bác sĩ có nhiều bệnh nhân",
            font=("San Francisco", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            pady=10
        ).pack()

        doctor_tree = ttk.Treeview(doctor_frame, columns=("doctor", "count"),
                                   show="headings", height=8)
        doctor_tree.heading("doctor", text="Bác sĩ")
        doctor_tree.heading("count", text="Số bệnh nhân")
        doctor_tree.column("doctor", width=200, anchor="w")
        doctor_tree.column("count", width=100, anchor="center")

        doctor_data = Report.get_doctor_workload()
        for item in doctor_data:
            doctor_tree.insert("", "end", values=(
                item.get('bacSi', 'N/A'),
                item.get('so_benh_nhan', 0)
            ))

        doctor_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))