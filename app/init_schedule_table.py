# init_schedule_table.py
"""Script khởi tạo bảng schedule trong database"""


from app.models.Schedule import Schedule


if __name__ == "__main__":
    print("Đang khởi tạo bảng schedule...")
    Schedule.create_table()
    print("Hoàn tất!")