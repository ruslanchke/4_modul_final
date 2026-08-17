import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from entities.roles import Roles
from models.base_models import TestUser, RegisterUserResponse
from models.base_models import TestUser as TestUserModel


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()

    return {
        "id": response["id"],
        "email": response["email"],
        "password": test_user.password
    }

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
def movie(super_admin):

    movie_data = DataGenerator.generate_movie_data()

    response = super_admin.api.movies_api.create_movie(movie_data)

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def movie_factory(super_admin):

    created_movies = []

    def _create_movie(**kwargs):

        movie_data = DataGenerator.generate_movie_data(
            **kwargs
        )

        response = super_admin.api.movies_api.create_movie(movie_data)
        assert response.status_code == 201

        movie = response.json()

        created_movies.append(movie["id"])

        return movie

    yield _create_movie

    for movie_id in created_movies:
        response = super_admin.api.movies_api.delete_movie(movie_id)
        assert response.status_code in [200, 404]

@pytest.fixture
def user_factory(super_admin):
    created_users = []

    def _create_user(**kwargs):
        password = DataGenerator.generate_random_password()

        user_data = TestUserModel(
            email=DataGenerator.generate_random_email(),
            fullName=DataGenerator.generate_random_name(),
            password=password,
            passwordRepeat=password,
            roles=[Roles.USER],
            **kwargs
        )

        response = super_admin.api.auth_api.register_user(user_data)
        assert response.status_code == 201

        user = RegisterUserResponse.model_validate(response.json())
        created_users.append(user.id)

        return user

    yield _create_user

    super_admin.api.user_api.delete_users(*created_users)

@pytest.fixture
def admin_user(user_session, super_admin, creation_admin_data):
    new_session = user_session()

    admin_user = User(
        creation_admin_data["email"],
        creation_admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )

    response = super_admin.api.user_api.create_user(creation_admin_data)
    assert response.status_code == 201

    print("ADMIN DATA:", creation_admin_data)
    print("CREATED USER:", response.json())

    user_id = response.json()["id"]

    update_data = {
        "roles": [Roles.ADMIN.value],
        "verified": True,
        "banned": False
    }

    response = super_admin.api.user_api.update_user(
        user_id,
        update_data
    )
    assert response.status_code == 200

    print("UPDATED USER:", response.json())

    admin_user.api.auth_api.authenticate(admin_user.creds)

    yield admin_user

    super_admin.api.user_api.delete_user(user_id)

@pytest.fixture
def auth_api(api_manager):
    return api_manager.auth_api

@pytest.fixture
def login_data():
    return {
        "email": SuperAdminCreds.USERNAME,
        "password": SuperAdminCreds.PASSWORD
    }

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> dict:
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False
        }
    ).model_dump()

@pytest.fixture(scope="function")
def creation_admin_data(creation_user_data):
    updated_data = creation_user_data.copy()
    updated_data["roles"] = [Roles.ADMIN.value]
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )

    response = super_admin.api.user_api.create_user(creation_user_data)
    assert response.status_code == 201

    user_id = response.json()["id"]

    common_user.api.auth_api.authenticate(common_user.creds)

    yield common_user

    super_admin.api.user_api.delete_user(user_id)

@pytest.fixture
def unauthenticated_api_manager():
    session = requests.Session()

    api_manager = ApiManager(session)

    yield api_manager

    session.close()

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }