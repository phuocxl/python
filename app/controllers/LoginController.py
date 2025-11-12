# app/controllers/login_controller.py
from app.models.UserModel import User

class LoginController:
    @staticmethod
    def login(username: str, password: str) -> dict:
        """
        Xử lý đăng nhập.
        Trả về dict:
        - {"success": True, "user": user} nếu đăng nhập thành công
        - {"success": False, "message": "..."} nếu thất bại
        """
        # Kiểm tra input
        if not username.strip() or not password.strip():
            return {"success": False, "message": "Vui lòng nhập đầy đủ thông tin"}

        # Kiểm tra user & password
        user = User.check_user(username, password)
        if not user:
            return {"success": False, "message": "Sai username hoặc mật khẩu"}

        # Login thành công
        return {"success": True, "user": user}
