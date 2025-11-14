from app.models.UserModel import User

class UserController:
    """Controller quản lý User"""

    @staticmethod
    def get_all_users():
        return User.get_all_users()  # trả về list dict: id, username, role, email

    @staticmethod
    def create_user(data: dict) -> bool:
        return User.add_user(
            username=data.get("username"),
            password=data.get("password", "123456"),  # mặc định password
            email=data.get("email"),
            role=data.get("role"),
            status="active"
        )

    @staticmethod
    def update_user(user_id, data: dict) -> bool:
        password = data.get("password")
        return User.update_user(
            user_id,
            data.get("username"),
            password,
            data.get("email"),
            data.get("role"),
            "active"
        )

    @staticmethod
    def delete_user(user_id: int) -> bool:
        return User.delete_user_db(user_id)
