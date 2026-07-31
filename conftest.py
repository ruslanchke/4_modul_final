import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user):

    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()

    print(response_data)

    api_manager.auth_api.authenticate(
        (
            test_user["email"],
            test_user["password"]
        )
    )

    return {
        **test_user,
        "id": response_data["id"]
    }

@pytest.fixture
def movie(authenticated_user, api_manager):

    movie_data = DataGenerator.generate_movie_data()

    response = api_manager.movies_api.create_movie(movie_data)

    return response.json()

@pytest.fixture(scope="function")
def admin_user(api_manager):

    user_data = {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }

    api_manager.auth_api.authenticate(
        (
            user_data["email"],
            user_data["password"]
        )
    )

    return user_data

@pytest.fixture
def auth_api(api_manager):
    return api_manager.auth_api

@pytest.fixture
def login_data():
    return {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }