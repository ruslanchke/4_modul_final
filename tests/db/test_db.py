from db_models.user import UserDBModel
from db_requester.db_client import check_db_connection
from utils.data_generator import DataGenerator


def test_db_connection():
    check_db_connection()

    # Можете сделать рандомный тестовый файл для проверки работы фикстуры
    # Так сказать - поиграться


def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

def test_movie_lifecycle(super_admin, db_helper):
    movie_data = DataGenerator.generate_movie_data()

    assert db_helper.get_movie_by_name(movie_data["name"]) is None

    response = super_admin.api.movies_api.create_movie(movie_data)
    assert response.status_code == 201

    movie = response.json()
    movie_id = movie["id"]

    movie_from_db = db_helper.get_movie_by_id(movie_id)

    assert movie_from_db is not None
    assert movie_from_db.name == movie_data["name"]

    response = super_admin.api.movies_api.delete_movie(movie_id)
    assert response.status_code == 200

    assert db_helper.get_movie_by_id(movie_id) is None