from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from .db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    hashed_password = Column(String)
    username = Column(String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
