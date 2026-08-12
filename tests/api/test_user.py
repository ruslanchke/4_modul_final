from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds

def test_delete_users(api_manager):
    api_manager.auth_api.authenticate(
        (
            SuperAdminCreds.USERNAME,
            SuperAdminCreds.PASSWORD
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


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

def test_get_user_by_id_common_user(common_user):
        response = common_user.api.user_api.get_user(common_user.email)
        assert response.status_code == 403
