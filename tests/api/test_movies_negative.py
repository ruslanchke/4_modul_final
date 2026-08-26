import allure
import pytest

from utils.data_generator import DataGenerator


@allure.epic("Cinescope API")
@allure.feature("Movies API - Негативные сценарии")
@allure.story("Создание фильма без обязательного поля")
@allure.title("Создание фильма без названия")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_create_movie_without_name(api_manager, admin_user):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Удалить обязательное поле name"):
        movie_data.pop("name")

    with allure.step("Отправить запрос на создание фильма"):
        response = api_manager.movies_api.create_movie(
            movie_data
        )

    with allure.step("Проверить статус-код 400"):
        assert response.status_code == 400

    body = response.json()

    with allure.step("Проверить сообщение об отсутствии name"):
        assert "name should not be empty" in body["message"]


@allure.epic("Cinescope API")
@allure.feature("Movies API - Негативные сценарии")
@allure.story("Получение фильма с некорректным ID")
@allure.title("Получение фильма по несуществующему ID")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_get_movie_by_invalid_id(api_manager, admin_user):

    with allure.step("Отправить запрос с несуществующим ID фильма"):
        response = api_manager.movies_api.get_movie(
            movie_id=999999999
        )

    with allure.step("Проверить статус-код 404"):
        assert response.status_code == 404

    body = response.json()

    with allure.step("Проверить statusCode в ответе"):
        assert body["statusCode"] == 404


@allure.epic("Cinescope API")
@allure.feature("Movies API - Авторизация")
@allure.story("Создание фильма без авторизации")
@allure.title("Создание фильма без access token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.auth
def test_create_movie_without_token(unauthenticated_api_manager):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Отправить запрос без access token"):
        response = unauthenticated_api_manager.movies_api.create_movie(
            movie_data
        )

    with allure.step("Проверить статус-код 401"):
        assert response.status_code == 401


@allure.epic("Cinescope API")
@allure.feature("Movies API - Авторизация")
@allure.story("Ограничение доступа для обычного пользователя")
@allure.title("Обычный пользователь не может создать фильм")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.auth
def test_common_user_cannot_create_movie(common_user):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Попытаться создать фильм от имени обычного пользователя"):
        response = common_user.api.movies_api.create_movie(movie_data)

    with allure.step("Проверить статус-код 403"):
        assert response.status_code == 403

    response_body = response.json()

    with allure.step("Проверить тело ответа"):
        assert response_body["error"] == "Forbidden"
        assert response_body["message"] == "Forbidden resource"

    with allure.step("Получить список фильмов"):
        movies_response = common_user.api.movies_api.get_movies()

    with allure.step("Проверить статус-код получения списка фильмов"):
        assert movies_response.status_code == 200

    movies = movies_response.json()["movies"]

    with allure.step("Проверить, что фильм не был создан"):
        assert not any(
            movie["name"] == movie_data["name"]
            for movie in movies
        )


@allure.epic("Cinescope API")
@allure.feature("Movies API - Авторизация")
@allure.story("Ограничение удаления для обычного пользователя")
@allure.title("Обычный пользователь не может удалить фильм")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.auth
def test_common_user_cannot_delete_movie(super_admin, common_user):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Создать фильм от имени супер-администратора"):
        create_response = super_admin.api.movies_api.create_movie(movie_data)

    movie_id = create_response.json()["id"]

    with allure.step("Попытаться удалить фильм от имени обычного пользователя"):
        delete_response = common_user.api.movies_api.delete_movie(
            movie_id
        )

    with allure.step("Проверить статус-код 403"):
        assert delete_response.status_code == 403

    body = delete_response.json()

    with allure.step("Проверить тело ответа"):
        assert body["message"] == "Forbidden resource"
        assert body["error"] == "Forbidden"
        assert body["statusCode"] == 403

    with allure.step("Проверить, что фильм не был удалён"):
        get_response = super_admin.api.movies_api.get_movie(movie_id)

        assert get_response.status_code == 200
        assert get_response.json()["id"] == movie_id


@allure.epic("Cinescope API")
@allure.feature("Movies API - Авторизация")
@allure.story("Удаление фильма без авторизации")
@allure.title("Удаление фильма без access token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.auth
def test_delete_movie_without_token(super_admin, user_session):

    with allure.step("Сгенерировать данные фильма"):
        movie_data = DataGenerator.generate_movie_data()

    with allure.step("Создать фильм от имени супер-администратора"):
        create_response = super_admin.api.movies_api.create_movie(movie_data)

    with allure.step("Проверить успешное создание фильма"):
        assert create_response.status_code == 201

    movie_id = create_response.json()["id"]

    with allure.step("Создать API-клиент без авторизации"):
        api = user_session()

    with allure.step("Попытаться удалить фильм без access token"):
        delete_response = api.movies_api.delete_movie(movie_id)

    with allure.step("Проверить статус-код 401"):
        assert delete_response.status_code == 401

    body = delete_response.json()

    with allure.step("Проверить тело ответа"):
        assert body["message"] == "Unauthorized"
        assert body["statusCode"] == 401

    with allure.step("Проверить, что фильм не был удалён"):
        get_response = super_admin.api.movies_api.get_movie(movie_id)

        assert get_response.status_code == 200
        assert get_response.json()["id"] == movie_id