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