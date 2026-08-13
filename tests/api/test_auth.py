import requests
import pytest
from resources.user_creds import SuperAdminCreds
from models.base_models import RegisterUserResponse


class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)

        assert response.status_code == 201

        RegisterUserResponse.model_validate(response.json())

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data)

        assert "accessToken" in response.json()


def test_get_user_info(api_manager):

    api_manager.auth_api.authenticate(
        (
            SuperAdminCreds.USERNAME,
            SuperAdminCreds.PASSWORD
        )
    )

    response = api_manager.user_api.get_user_info(SuperAdminCreds.USERNAME)

    user = RegisterUserResponse.model_validate(response.json())

    assert user.email == SuperAdminCreds.USERNAME

