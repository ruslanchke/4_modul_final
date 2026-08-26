import allure
import pytest

from models.base_models import RegisterUserResponse


@allure.epic("Cinescope API")
@allure.feature("User API")
@allure.story("Удаление пользователей")
@allure.title("Удаление нескольких пользователей")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.crud
def test_delete_users(user_factory, super_admin):

    with allure.step("Создать трех тестовых пользователей"):
        users = [user_factory() for _ in range(3)]

    with allure.step("Удалить созданных пользователей"):
        super_admin.api.user_api.delete_users(
            *(user.id for user in users)
        )


class TestUser:

    @allure.epic("Cinescope API")
    @allure.feature("User API")
    @allure.story("Создание пользователя")
    @allure.title("Создание нового пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_create_user(self, super_admin, creation_user_data):

        with allure.step("Создать пользователя"):
            response = super_admin.api.user_api.create_user(
                creation_user_data
            )

        with allure.step("Проверить статус-код 201"):
            assert response.status_code == 201

        with allure.step("Провалидировать схему ответа"):
            RegisterUserResponse.model_validate(
                response.json()
            )


    @allure.epic("Cinescope API")
    @allure.feature("User API")
    @allure.story("Получение пользователя")
    @allure.title("Получение пользователя по ID и email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_get_user_by_locator(self, user_factory, super_admin):

        with allure.step("Создать тестового пользователя"):
            created_user = user_factory()

        with allure.step("Получить пользователя по ID"):
            user_by_id = RegisterUserResponse.model_validate(
                super_admin.api.user_api.get_user(
                    created_user.id
                ).json()
            )

        with allure.step("Получить пользователя по email"):
            user_by_email = RegisterUserResponse.model_validate(
                super_admin.api.user_api.get_user(
                    created_user.email
                ).json()
            )

        with allure.step("Сравнить пользователей"):
            assert user_by_id == user_by_email


@allure.epic("Cinescope API")
@allure.feature("User API - Авторизация")
@allure.story("Ограничение доступа обычного пользователя")
@allure.title("Обычный пользователь не может получить данные пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.auth
def test_get_user_by_id_common_user(common_user):

    with allure.step("Попытаться получить данные пользователя"):
        response = common_user.api.user_api.get_user(
            common_user.email
        )

    with allure.step("Проверить статус-код 403"):
        assert response.status_code == 403