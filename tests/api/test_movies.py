from utils.data_generator import DataGenerator

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


def test_create_movie(admin_user, api_manager):

    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    body = response.json()

    assert body["id"] != ""
    assert body["name"] == movie_data["name"]
    assert body["price"] == movie_data["price"]
    assert body["description"] == movie_data["description"]
    assert body["location"] == movie_data["location"]
    assert body["published"] == movie_data["published"]
    assert body["genreId"] == movie_data["genreId"]
    assert body["imageUrl"] == movie_data["imageUrl"]

def test_get_movie_by_id(admin_user, api_manager):
    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    body = response.json()
    movie_id = body["id"]

    response = api_manager.movies_api.get_movie(movie_id)
    assert response.status_code == 200

    body = response.json()

    assert body["id"] == movie_id
    assert body["name"] == movie_data["name"]
    assert body["price"] == movie_data["price"]
    assert body["description"] == movie_data["description"]
    assert body["location"] == movie_data["location"]
    assert body["published"] == movie_data["published"]
    assert body["genreId"] == movie_data["genreId"]
    assert body["imageUrl"] == movie_data["imageUrl"]

def test_delete_movie_by_id(admin_user, api_manager):
    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    body = response.json()
    movie_id = body["id"]

    response = api_manager.movies_api.delete_movie(movie_id)
    assert response.status_code == 200

    api_manager.movies_api.get_movie(
        movie_id
    )

def test_patch_movie_by_id(api_manager, admin_user):
    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    movie_id = response.json()["id"]
    update_data = DataGenerator.generate_update_movie_data()

    response = api_manager.movies_api.update_movie(
        movie_id,
        update_data
    )
    assert response.status_code == 200

    response = api_manager.movies_api.get_movie(movie_id)
    assert response.status_code == 200

    body = response.json()

    assert body["id"] == movie_id
    assert body["name"] == update_data["name"]
    assert body["price"] == movie_data["price"]
    assert body["description"] == movie_data["description"]
    assert body["location"] == movie_data["location"]
    assert body["published"] == movie_data["published"]
    assert body["genreId"] == movie_data["genreId"]
    assert body["imageUrl"] == movie_data["imageUrl"]

def test_get_movies_by_location_filter(api_manager):

    response = api_manager.movies_api.get_movies(
        params={
            "locations": "SPB"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["movies"]) > 0

    for movie in body["movies"]:
        assert movie["location"] == "SPB"