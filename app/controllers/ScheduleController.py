# app/controllers/ScheduleController.py
from app.models.Schedule import Schedule


class ScheduleController:
    """Controller quản lý lịch làm việc"""


    @staticmethod
    def get_all_schedules():
        """Lấy tất cả lịch làm việc"""
        return Schedule.get_all_schedules()


    @staticmethod
    def create_schedule(data: dict) -> bool:
        """Tạo lịch làm việc mới"""
        return Schedule.add_schedule(
            ma_bacsi=data.get("ma_bacsi"),
            ngay_lam_viec=data.get("ngay_lam_viec"),
            gio_bat_dau=data.get("gio_bat_dau"),
            gio_ket_thuc=data.get("gio_ket_thuc"),
            ghi_chu=data.get("ghi_chu", "")
        )


    @staticmethod
    def update_schedule(ma_lich, data: dict) -> bool:
        """Cập nhật lịch làm việc"""
        return Schedule.update_schedule(
            ma_lich=ma_lich,
            ma_bacsi=data.get("ma_bacsi"),
            ngay_lam_viec=data.get("ngay_lam_viec"),
            gio_bat_dau=data.get("gio_bat_dau"),
            gio_ket_thuc=data.get("gio_ket_thuc"),
            trang_thai=data.get("trang_thai", "active"),
            ghi_chu=data.get("ghi_chu", "")
        )


    @staticmethod
    def delete_schedule(ma_lich: int) -> bool:
        """Xóa lịch làm việc"""
        return Schedule.delete_schedule(ma_lich)


    @staticmethod
    def get_schedule_by_doctor(ma_bacsi: int):
        """Lấy lịch theo bác sĩ"""
        return Schedule.get_schedule_by_doctor(ma_bacsi)


    @staticmethod
    def get_schedule_by_date(ngay_lam_viec):
        """Lấy lịch theo ngày"""
        return Schedule.get_schedule_by_date(ngay_lam_viec)
