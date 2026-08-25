from db_models.user import Base
from sqlalchemy import Column, String, Integer


class AccountTransactionTemplate(Base):
    __tablename__ = "accounts_transaction_template"

    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)