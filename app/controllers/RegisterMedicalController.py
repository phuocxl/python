from app.models.RegisterMedical import RegisterMedical


class RegisterMedicalController:

    @staticmethod
    def get_all_registers():
        return RegisterMedical.get_all_registers()

    @staticmethod
    def create_register(data: dict):
        return RegisterMedical.add_register(data)

    @staticmethod
    def update_register(madangky, data: dict):
        return RegisterMedical.update_register(madangky, data)

    @staticmethod
    def delete_register(madangky: int) -> bool:
        return RegisterMedical.delete_register(madangky)

    @staticmethod
    def get_register_by_id(madangky: int):
        return RegisterMedical.get_register_by_id(madangky)
