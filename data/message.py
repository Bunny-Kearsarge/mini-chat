from sqlalchemy import Column, String, Integer
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement='True')
    text = Column(String)
