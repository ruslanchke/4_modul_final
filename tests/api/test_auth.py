import allure
import pytest
from entities.roles import Roles
from resources.user_creds import SuperAdminCreds
from models.base_models import RegisterUserResponse


class TestAuth:

    @pytest.mark.auth
    @pytest.mark.smoke
    @allure.epic("Cinescope API")
    @allure.feature("Auth API")
    @allure.story("Регистрация пользователя")
    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_user(self, api_manager, test_user):

        with allure.step("Зарегистрировать нового пользователя"):
            response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверить статус-код 201"):
            assert response.status_code == 201

        with allure.step("Провалидировать схему ответа"):
            user = RegisterUserResponse.model_validate(response.json())

        with allure.step("Проверить данные зарегистрированного пользователя"):
            assert user.email == test_user.email
            assert user.fullName == test_user.fullName
            assert user.roles == [Roles.USER]
            assert user.verified is True

    @pytest.mark.auth
    @pytest.mark.smoke
    @allure.epic("Cinescope API")
    @allure.feature("Auth API")
    @allure.story("Авторизация пользователя")
    @allure.title("Регистрация и авторизация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_and_login_user(self, api_manager, registered_user):

        with allure.step("Подготовить данные для авторизации"):
            login_data = {
                "email": registered_user["email"],
                "password": registered_user["password"]
            }

        with allure.step("Авторизовать пользователя"):
            response = api_manager.auth_api.login_user(login_data)

        with allure.step("Проверить наличие accessToken"):
            assert "accessToken" in response.json()

@allure.epic("Cinescope API")
@allure.feature("User API")
@allure.story("Получение информации о пользователе")
@allure.title("Получение информации о супер-администраторе")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.auth
def test_get_user_info(api_manager):

    with allure.step("Авторизоваться под супер-администратором"):
        api_manager.auth_api.authenticate(
            (
                SuperAdminCreds.USERNAME,
                SuperAdminCreds.PASSWORD
            )
        )

    with allure.step("Получить информацию о пользователе"):
        response = api_manager.user_api.get_user_info(SuperAdminCreds.USERNAME)

    with allure.step("Провалидировать схему ответа"):
        user = RegisterUserResponse.model_validate(response.json())

    with allure.step("Проверить email пользователя"):
        assert user.email == SuperAdminCreds.USERNAME

