import allure
import pytest

from db_requester.db_client import check_db_connection
from utils.data_generator import DataGenerator


@allure.epic("Cinescope API")
@allure.feature("Database")
@allure.story("Проверка подключения к базе данных")
@allure.title("Проверка соединения с базой данных")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.db
def test_db_connection():

    with allure.step("Проверить подключение к базе данных"):
        check_db_connection()


@allure.epic("Cinescope API")
@allure.feature("Database")
@allure.story("Работа с пользователями в базе данных")
@allure.title("Проверка получения пользователя из базы данных")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.db
def test_db_requests(super_admin, db_helper, created_test_user):

    with allure.step("Получить пользователя из базы данных по ID"):
        user_from_db = db_helper.get_user_by_id(
            created_test_user.id
        )

    with allure.step("Сравнить созданного пользователя с пользователем из БД"):
        assert created_test_user == user_from_db

    with allure.step("Проверить наличие пользователя по email"):
        assert db_helper.user_exists_by_email(
            "api1@gmail.com"
        )


@allure.epic("Cinescope API")
@allure.feature("Database")
@allure.story("Жизненный цикл фильма")
@allure.title("Создание и удаление фильма с проверкой БД")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.db
def test_movie_lifecycle(super_admin, db_helper):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Проверить отсутствие фильма в БД"):
        assert db_helper.get_movie_by_name(
            movie_data["name"]
        ) is None

    with allure.step("Создать фильм через API"):
        response = super_admin.api.movies_api.create_movie(
            movie_data
        )

    with allure.step("Проверить успешное создание фильма"):
        assert response.status_code == 201

    movie = response.json()
    movie_id = movie["id"]

    with allure.step("Получить созданный фильм из БД"):
        movie_from_db = db_helper.get_movie_by_id(movie_id)

    with allure.step("Проверить наличие фильма в БД"):
        assert movie_from_db is not None

    with allure.step("Проверить название фильма в БД"):
        assert movie_from_db.name == movie_data["name"]

    with allure.step("Удалить фильм через API"):
        response = super_admin.api.movies_api.delete_movie(
            movie_id
        )

    with allure.step("Проверить успешное удаление фильма"):
        assert response.status_code == 200

    with allure.step("Проверить отсутствие фильма в БД"):
        assert db_helper.get_movie_by_id(movie_id) is None