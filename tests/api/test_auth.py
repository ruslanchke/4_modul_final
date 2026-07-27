import requests
import pytest
from custom_requester.custom_requester import CustomRequester
from data.auth.register_data import get_register_payload


class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    def test_register_timeout(self, api_manager, test_user):
        with pytest.raises(requests.exceptions.ReadTimeout):
            api_manager.auth_api.register_user(
                test_user,
                timeout=0.001
            )

def test_logout(auth_api, login_data):

    login_response = auth_api.login_user(login_data)

    token = login_response.json()["accessToken"]

    auth_api.update_session_headers({
        "Authorization": f"Bearer {token}"
    })

    print("AFTER TOKEN UPDATE:")
    print(auth_api.session.headers)

    response = auth_api.logout_user()

    assert response.status_code == 200


def test_authenticated_user(authenticated_user):
    print(authenticated_user)

def test_get_user_info(api_manager):

    api_manager.auth_api.authenticate(
        ("api1@gmail.com", "asdqwe123Q")
    )

    response = api_manager.user_api.get_user_info("api1@gmail.com")
    response_data = response.json()

    assert response_data["email"] == "api1@gmail.com"

