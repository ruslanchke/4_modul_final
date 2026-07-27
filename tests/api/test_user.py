from utils.data_generator import DataGenerator

def test_delete_users(api_manager):
    api_manager.auth_api.authenticate(
        (
            "api1@gmail.com",
            "asdqwe123Q"
        )
    )

    user_ids = []

    for _ in range(3):

        password = DataGenerator.generate_random_password()

        user_data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"]
        }

        print(user_data["email"])

        response = api_manager.auth_api.register_user(user_data)

        user_ids.append(response.json()["id"])


    api_manager.user_api.delete_users(
        *user_ids
    )