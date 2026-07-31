from utils.data_generator import DataGenerator

def test_create_movie_without_name(api_manager, admin_user):
    movie_data = DataGenerator.generate_movie_data()
    movie_data.pop("name")

    response = api_manager.movies_api.create_movie(
        movie_data,
        expected_status=400
    )

def test_get_movie_by_invalid_id(api_manager, admin_user):
    response = api_manager.movies_api.get_movie(
        movie_id=999999999,
        expected_status=404
    )

    assert response.status_code == 404