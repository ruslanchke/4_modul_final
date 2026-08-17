from utils.data_generator import DataGenerator
import pytest

def test_get_movies(api_manager):

    response = api_manager.movies_api.get_movies()

    assert response.status_code == 200
    body = response.json()

    # Проверка структуры ответа
    assert "movies" in body
    assert "count" in body
    assert "page" in body
    assert "pageSize" in body
    assert "pageCount" in body

    # Проверка пагинации
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


def test_create_movie(movie_factory):

    movie = movie_factory(
        location="MSK",
        published=False,
        genre_id=5
    )

    assert movie["id"] is not None
    assert movie["location"] == "MSK"
    assert movie["published"] is False
    assert movie["genreId"] == 5

def test_get_movie_by_id(api_manager, movie_factory):

    movie = movie_factory()

    response = api_manager.movies_api.get_movie(
        movie["id"]
    )
    assert response.status_code == 200

    body = response.json()

    assert body["id"] == movie["id"]
    assert body["name"] == movie["name"]
    assert body["price"] == movie["price"]
    assert body["description"] == movie["description"]
    assert body["location"] == movie["location"]
    assert body["published"] == movie["published"]
    assert body["genreId"] == movie["genreId"]
    assert body["imageUrl"] == movie["imageUrl"]

def test_delete_movie_by_id(super_admin, movie_factory):

    movie = movie_factory()
    movie_id = movie["id"]

    response = super_admin.api.movies_api.delete_movie(movie_id)
    assert response.status_code == 200

    response = super_admin.api.movies_api.get_movie(movie_id)
    assert response.status_code == 404

def test_patch_movie_by_id(super_admin, movie_factory):

    movie = movie_factory()
    movie_id = movie["id"]

    update_data = DataGenerator.generate_update_movie_data()
    response = super_admin.api.movies_api.update_movie(
        movie_id,
        update_data
    )

    assert response.status_code == 200

    response = super_admin.api.movies_api.get_movie(movie_id)
    assert response.status_code == 200

    body = response.json()

    assert body["id"] == movie_id
    assert body["name"] == update_data["name"]
    assert body["price"] == movie["price"]
    assert body["description"] == movie["description"]
    assert body["location"] == movie["location"]
    assert body["published"] == movie["published"]
    assert body["genreId"] == movie["genreId"]
    assert body["imageUrl"] == movie["imageUrl"]

def test_get_movies_by_location_filter(api_manager, movie_factory):

    movie = movie_factory(
        location="SPB"
    )

    response = api_manager.movies_api.get_movies(
        params={
            "locations": "SPB",
            "createdAt": "desc"
        }
    )

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body["movies"], list)

    created_movie = next(
        movie_item for movie_item in body["movies"]
        if movie_item["id"] == movie["id"]
    )

    assert created_movie["id"] == movie["id"]
    assert created_movie["name"] == movie["name"]
    assert created_movie["price"] == movie["price"]
    assert created_movie["description"] == movie["description"]
    assert created_movie["location"] == movie["location"]
    assert created_movie["published"] == movie["published"]
    assert created_movie["genreId"] == movie["genreId"]
    assert created_movie["imageUrl"] == movie["imageUrl"]



def test_get_movies_by_filter(api_manager, movie_factory):
    movie_factory(price=99)
    movie_factory(price=100)
    movie_factory(price=300)
    movie_factory(price=500)
    movie_factory(price=501)

    response = api_manager.movies_api.get_movies(
        params={"minPrice": 100, "maxPrice": 500}
    )

    assert response.status_code == 200

    movies = response.json()["movies"]

    assert all(100 <= movie["price"] <= 500 for movie in movies)


@pytest.mark.parametrize(
    "role, expected_status",
    [
        ("super_admin", 200),
        ("admin_user", 403),
        ("common_user", 403),
    ]
)

def test_delete_movie_by_role(request, movie_factory, role, expected_status):
    movie = movie_factory()

    user = request.getfixturevalue(role)

    response = user.api.movies_api.delete_movie(movie["id"])

    assert response.status_code == expected_status