from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from models.base_models import RegisterUserResponse
from models.base_models import TestUser as TestUserModel
from entities.roles import Roles

def test_delete_users(user_factory, super_admin):
    users = [user_factory() for _ in range(3)]

    super_admin.api.user_api.delete_users(
        *(user.id for user in users)
    )

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)

        assert response.status_code == 201

        RegisterUserResponse.model_validate(response.json())

    def test_get_user_by_locator(self, user_factory, super_admin):
        created_user = user_factory()

        user_by_id = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(created_user.id).json()
        )

        user_by_email = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(created_user.email).json()
        )

        assert user_by_id == user_by_email

def test_get_user_by_id_common_user(common_user):
        response = common_user.api.user_api.get_user(common_user.email)
        assert response.status_code == 403
