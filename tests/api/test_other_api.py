import pytest

from db_models.models import AccountTransactionTemplate
from faker import Faker

from db_models.movies import MovieDBModel
from datetime import datetime

fake = Faker()


def test_accounts_transaction_template(db_session):
    # Подготовка тестовых данных
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

        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        from_account.balance -= amount
        to_account.balance += amount

        session.commit()

    try:
        # Проверяем начальные балансы
        assert stan.balance == 100
        assert bob.balance == 500

        # Пытаемся перевести 200, хотя у Stan только 100
        with pytest.raises(ValueError, match="Недостаточно средств"):
            transfer_money(
                db_session,
                from_account_name=stan.user,
                to_account_name=bob.user,
                amount=200
            )

        # Проверяем, что балансы не изменились
        db_session.refresh(stan)
        db_session.refresh(bob)

        assert stan.balance == 100
        assert bob.balance == 500

        # Проверяем, что общая сумма денег тоже не изменилась
        assert stan.balance + bob.balance == 600

    finally:
        # Удаляем тестовые данные
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