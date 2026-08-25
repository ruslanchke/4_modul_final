import datetime
import uuid

from faker import Faker


class DataGenerator:
    fake = Faker()

    @staticmethod
    def generate_random_email():
        return f"{uuid.uuid4()}@example.com"

    @staticmethod
    def generate_random_name():
        return DataGenerator.fake.name()

    @staticmethod
    def generate_random_password():
        return "Test1234@"

    @staticmethod
    def generate_movie_data(
            location="SPB",
            published=True,
            genre_id=5,
            price=None
    ):
        return {
            "name": DataGenerator.fake.catch_phrase(),
            "imageUrl": "https://image.url",
            "price": price if price is not None else DataGenerator.fake.random_int(min=100, max=1000),
            "description": DataGenerator.fake.text(max_nb_chars=50),
            "location": location,
            "published": published,
            "genreId": genre_id
        }

    @staticmethod
    def generate_update_movie_data():
        return {
            "name": DataGenerator.fake.catch_phrase()
        }

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }