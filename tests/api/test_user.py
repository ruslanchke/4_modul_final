from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from models.base_models import RegisterUserResponse
from models.base_models import TestUser as TestUserModel
from entities.roles import Roles

def test_delete_users(api_manager):
    api_manager.auth_api.authenticate(
        (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)
    )

    user_ids = []

    for _ in range(3):
        password = DataGenerator.generate_random_password()

        user_data = TestUserModel(
            email=DataGenerator.generate_random_email(),
            fullName=DataGenerator.generate_random_name(),
            password=password,
            passwordRepeat=password,
            roles=[Roles.USER]
        )

        response = api_manager.auth_api.register_user(user_data)

        assert response.status_code == 201
        created_user = RegisterUserResponse.model_validate(response.json())
        user_ids.append(created_user.id)

    api_manager.user_api.delete_users(*user_ids)

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)

        assert response.status_code == 201

        RegisterUserResponse.model_validate(response.json())

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user = super_admin.api.user_api.create_user(creation_user_data).json()

        user_by_id = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(created_user["id"]).json())

        user_by_email = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(creation_user_data["email"]).json())

        assert user_by_id == user_by_email

def test_get_user_by_id_common_user(common_user):
        response = common_user.api.user_api.get_user(common_user.email)
        assert response.status_code == 403
