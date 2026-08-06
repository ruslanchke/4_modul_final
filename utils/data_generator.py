from faker import Faker


class DataGenerator:
    fake = Faker()

    @staticmethod
    def generate_random_email():
        return DataGenerator.fake.email()

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
            genre_id=1
    ):
        return {
            "name": DataGenerator.fake.catch_phrase(),
            "imageUrl": "https://image.url",
            "price": DataGenerator.fake.random_int(min=100, max=1000),
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