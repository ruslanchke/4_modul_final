import allure
import pytest

from db_models.models import AccountTransactionTemplate
from faker import Faker

from db_models.movies import MovieDBModel
from datetime import datetime

fake = Faker()

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Недостаточно средств для перевода")
    @allure.description("""
        Тест проверяет, что при попытке перевести сумму,
        превышающую баланс отправителя, перевод не выполняется,
        а балансы обоих счетов остаются без изменений.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ruslan AQA")
    @allure.title("Перевод невозможен при недостаточном балансе")

    def test_accounts_transaction_template(self, db_session):

        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(
                user=f"Stan_{fake.random_int(min=1, max=10000)}",
                balance=100
            )

            bob = AccountTransactionTemplate(
                user=f"Bob_{fake.random_int(min=1, max=10000)}",
                balance=500
            )

            db_session.add_all([stan, bob])
            db_session.commit()

        def transfer_money(session, from_account_name, to_account_name, amount):

            with allure.step("Получаем счета"):
                from_account = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=from_account_name)
                    .one()
                )

                to_account = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=to_account_name)
                    .one()
                )

            with allure.step("Проверяем достаточность средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        try:
            with allure.step("Проверяем начальные балансы"):
                assert stan.balance == 100
                assert bob.balance == 500

            with allure.step("Пытаемся перевести 200 единиц от Stan к Bob"):
                with pytest.raises(ValueError, match="Недостаточно средств на счете"):
                    transfer_money(
                        db_session,
                        from_account_name=stan.user,
                        to_account_name=bob.user,
                        amount=200
                    )

            db_session.refresh(stan)
            db_session.refresh(bob)

            with allure.step("Проверяем, что балансы не изменились"):
                assert stan.balance == 100
                assert bob.balance == 500

            with allure.step("Проверяем сохранение общей суммы денег"):
                assert stan.balance + bob.balance == 600

        finally:
            with allure.step("Удаляем тестовые данные из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()

def test_delete_movie(super_admin, db_session, movie_factory):
    # Создаём фильм через фабрику
    movie = movie_factory()
    movie_id = movie["id"]

    # Проверяем, что фильм появился в БД
    movie_before_delete = (
        db_session.query(MovieDBModel)
        .filter(MovieDBModel.id == movie_id)
        .first()
    )

    assert movie_before_delete is not None

    # Удаляем фильм через API
    response = super_admin.api.movies_api.delete_movie(movie_id)

    assert response.status_code == 200

    # Проверяем, что фильм удалён из БД
    movie_after_delete = (
        db_session.query(MovieDBModel)
        .filter(MovieDBModel.id == movie_id)
        .first()
    )

    assert movie_after_delete is None