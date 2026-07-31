from utils.data_generator import DataGenerator

def test_get_movies(api_manager):

    response = api_manager.movies_api.get_movies()

    assert response.status_code == 200

def test_create_movie(admin_user, api_manager):

    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    body = response.json()
    assert body["name"] == movie_data["name"]

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

def test_delete_movie_by_id(admin_user, api_manager):
    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    body = response.json()
    movie_id = body["id"]

    response = api_manager.movies_api.delete_movie(movie_id)
    assert response.status_code == 200

    api_manager.movies_api.get_movie(
        movie_id,
        expected_status=404
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

    assert body["name"] == update_data["name"]

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