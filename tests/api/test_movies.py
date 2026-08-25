import allure
from utils.data_generator import DataGenerator
import pytest

@allure.epic("Cinescope API")
@allure.feature("Movies API")
@allure.story("Получение списка фильмов")
@allure.title("Получение списка фильмов")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_get_movies(api_manager):
    with allure.step("Отправить GET-запрос на получение списка фильмов"):
        response = api_manager.movies_api.get_movies()

    with allure.step("Проверить статус-код 200"):
        assert response.status_code == 200

    with allure.step("Получить тело ответа"):
        body = response.json()

    with allure.step("Проверить структуру ответа"):
        assert "movies" in body
        assert "count" in body
        assert "page" in body
        assert "pageSize" in body
        assert "pageCount" in body

    with allure.step("Проверить пагинацию"):
        assert isinstance(body["count"], int)
        assert isinstance(body["page"], int)
        assert isinstance(body["pageSize"], int)
        assert isinstance(body["pageCount"], int)

    assert len(body["movies"]) > 0

    # Проверка структуры фильма
    movie = body["movies"][0]

    assert "id" in movie
    assert "name" in movie
    assert "description" in movie
    assert "genreId" in movie
    assert "imageUrl" in movie
    assert "price" in movie
    assert "rating" in movie
    assert "location" in movie
    assert "published" in movie
    assert "createdAt" in movie
    assert "genre" in movie

@allure.epic("Cinescope API")
@allure.feature("Movies API")
@allure.story("Создание фильма")
@allure.title("Создание фильма с валидными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.crud
def test_create_movie(movie_factory):

    with allure.step("Создать фильм"):
        movie = movie_factory(
            location="MSK",
            published=False,
            genre_id=5
        )

    with allure.step("Проверить данные созданного фильма"):
        assert movie["id"] is not None
        assert movie["location"] == "MSK"
        assert movie["published"] is False
        assert movie["genreId"] == 5

@allure.epic("Cinescope API")
@allure.feature("Movies API")
@allure.story("Получение фильма по ID")
@allure.title("Получение фильма по ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.crud
def test_get_movie_by_id(api_manager, movie_factory):

    with allure.step("Создать тестовый фильм"):
        movie = movie_factory()

    with allure.step(f"Получить фильм по ID: {movie['id']}"):
        response = api_manager.movies_api.get_movie(
            movie["id"]
        )

    with allure.step("Проверить статус-код 200"):
        assert response.status_code == 200

    body = response.json()

    with allure.step("Проверить данные фильма"):
        assert body["id"] == movie["id"]
        assert body["name"] == movie["name"]
        assert body["price"] == movie["price"]
        assert body["description"] == movie["description"]
        assert body["location"] == movie["location"]
        assert body["published"] == movie["published"]
        assert body["genreId"] == movie["genreId"]
        assert body["imageUrl"] == movie["imageUrl"]

@allure.epic("Cinescope API")
@allure.feature("Movies API")
@allure.story("Удаление фильма")
@allure.title("Удаление фильма по ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.crud
def test_delete_movie_by_id(super_admin, movie_factory):

    with allure.step("Создать тестовый фильм"):
        movie = movie_factory()

    movie_id = movie["id"]

    with allure.step(f"Удалить фильм с ID: {movie_id}"):
        response = super_admin.api.movies_api.delete_movie(movie_id)

    with allure.step("Проверить статус-код 200"):
        assert response.status_code == 200

    with allure.step(f"Проверить что фильм удален с ID: {movie_id}"):
        response = super_admin.api.movies_api.get_movie(movie_id)

    with allure.step("Проверить статус-код 404"):
        assert response.status_code == 404

@allure.epic("Cinescope API")
@allure.feature("Movies API")
@allure.story("Обновление фильма")
@allure.title("Обновление фильма по ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.crud
def test_patch_movie_by_id(super_admin, movie_factory):

    with allure.step("Создать тестовый фильм"):
        movie = movie_factory()

    movie_id = movie["id"]
    update_data = DataGenerator.generate_update_movie_data()

    with allure.step(f"Обновить фильм с ID: {movie_id}"):
        response = super_admin.api.movies_api.update_movie(
            movie_id,
            update_data
        )

    with allure.step("Проверить статус код: 200"):
        assert response.status_code == 200

    with allure.step("Получить обновлённый фильм"):
        response = super_admin.api.movies_api.get_movie(movie_id)

    with allure.step("Проверить статус код: 200"):
        assert response.status_code == 200

    body = response.json()

    with allure.step("Проверить обновлённые данные"):
        assert body["id"] == movie_id
        assert body["name"] == update_data["name"]
        assert body["price"] == movie["price"]
        assert body["description"] == movie["description"]
        assert body["location"] == movie["location"]
        assert body["published"] == movie["published"]
        assert body["genreId"] == movie["genreId"]
        assert body["imageUrl"] == movie["imageUrl"]

@allure.epic("Cinescope API")
@allure.feature("Movies API - Фильтрация")
@allure.story("Фильтрация фильмов по локации")
@allure.title("Получение фильмов с фильтром по локации")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.filters
def test_get_movies_by_location_filter(api_manager, movie_factory):

    with allure.step("Создать фильм с локацией SPB"):
        movie = movie_factory(
            location="SPB"
        )

    with allure.step("Получить фильмы с фильтром location=SPB"):
        response = api_manager.movies_api.get_movies(
            params={
                "locations": "SPB",
                "createdAt": "desc"
            }
        )

    with allure.step("Проверит статус код: 200"):
        assert response.status_code == 200

    body = response.json()

    with allure.step("Проверить, что список фильмов присутствует в ответе"):
        assert isinstance(body["movies"], list)

    with allure.step("Найти созданный фильм в результатах фильтрации"):
        created_movie = next(
            movie_item for movie_item in body["movies"]
            if movie_item["id"] == movie["id"]
        )
    with allure.step("Проверить данные найденного фильма"):
        assert created_movie["id"] == movie["id"]
        assert created_movie["name"] == movie["name"]
        assert created_movie["price"] == movie["price"]
        assert created_movie["description"] == movie["description"]
        assert created_movie["location"] == movie["location"]
        assert created_movie["published"] == movie["published"]
        assert created_movie["genreId"] == movie["genreId"]
        assert created_movie["imageUrl"] == movie["imageUrl"]

@allure.epic("Cinescope API")
@allure.feature("Movies API - Фильтрация")
@allure.story("Фильтрация фильмов по цене")
@allure.title("Получение фильмов в заданном ценовом диапазоне")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.filters
def test_get_movies_by_filter(api_manager, movie_factory):

    with allure.step("Создать фильмы с разными ценами"):
        movie_factory(price=99)
        movie_factory(price=100)
        movie_factory(price=300)
        movie_factory(price=500)
        movie_factory(price=501)

    with allure.step("Получить фильмы с ценой от 100 до 500"):
        response = api_manager.movies_api.get_movies(
            params={"minPrice": 100, "maxPrice": 500}
        )

    with allure.step("Проверить статус-код 200"):
        assert response.status_code == 200

    movies = response.json()["movies"]

    with allure.step("Проверить, что все фильмы находятся в заданном диапазоне"):
        assert all(100 <= movie["price"] <= 500 for movie in movies)

@pytest.mark.auth
@pytest.mark.parametrize(
    "role, expected_status",
    [
        ("super_admin", 200),
        ("admin_user", 403),
        ("common_user", 403),
    ]
)

@allure.epic("Cinescope API")
@allure.feature("Movies API - Авторизация")
@allure.story("Проверка удаления фильма в зависимости от роли")
@allure.title("Удаление фильма пользователем с ролью {role}")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_movie_by_role(request, movie_factory, role, expected_status):

    with allure.step("Создать тестовый фильм"):
        movie = movie_factory()

    with allure.step(f"Получить пользователя с ролью {role}"):
        user = request.getfixturevalue(role)

    with allure.step(f"Удалить фильм пользователем с ролью {role}"):
        response = user.api.movies_api.delete_movie(movie["id"])

    with allure.step(f"Проверить статус-код {expected_status}"):
        assert response.status_code == expected_status