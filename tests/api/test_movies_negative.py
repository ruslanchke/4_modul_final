from utils.data_generator import DataGenerator

def test_create_movie_without_name(api_manager, admin_user):
    movie_data = DataGenerator.generate_movie_data()
    movie_data.pop("name")

    response = api_manager.movies_api.create_movie(
        movie_data
    )

    assert response.status_code == 400

    body = response.json()

    assert "name should not be empty" in body["message"]

def test_get_movie_by_invalid_id(api_manager, admin_user):
    response = api_manager.movies_api.get_movie(
        movie_id=999999999
    )
    assert response.status_code == 404

    body = response.json()

    assert body["statusCode"] == 404


def test_create_movie_without_token(api_manager):
    movie_data = DataGenerator.generate_movie_data()

    api_manager.movies_api.create_movie(
        movie_data
    )


def test_common_user_cannot_create_movie(common_user):
    movie_data = DataGenerator.generate_movie_data()

    response = common_user.api.movies_api.create_movie(
        movie_data
    )
    assert response.status_code == 403

    response_body = response.json()
    assert response_body["error"] == "Forbidden"
    assert response_body["message"] == "Forbidden resource"


def test_common_user_cannot_delete_movie(super_admin, common_user):

    movie_data = DataGenerator.generate_movie_data()

    response = super_admin.api.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    movie_id = response.json()["id"]

    common_user.api.movies_api.delete_movie(
        movie_id
    )

def test_delete_movie_without_token(super_admin, user_session):

    movie_data = DataGenerator.generate_movie_data()

    response = super_admin.api.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    movie_id = response.json()["id"]

    api = user_session()

    api.movies_api.delete_movie(
        movie_id
    )