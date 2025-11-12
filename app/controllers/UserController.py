from app.models.UserModel import User


class UserController:
    @staticmethod
    def get_all_users():
        return User.get_all_users()

    @staticmethod
    def create_user(username, password, email, role, status):
        return User.add_user(username, password, email, role, status)

    @staticmethod
    def update_user(mauser, username, password, email, role, status):
        return User.update_user(mauser, username, password, email, role, status)

    @staticmethod
    def login(username, password):
        return User.check_user(username, password)

    @staticmethod
    def delete_user(ma_user: int) -> bool:
        """
        Xóa user đã chọn.
        Logic:
        - Không xóa user có role admin
        - Thông báo lỗi/thành công được xử lý trong Model
        """
        return User.delete_user_db(ma_user)
