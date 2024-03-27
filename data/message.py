from sqlalchemy import Column, String, Integer, ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Message(SqlAlchemyBase):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"))

    user = orm.relationship('User')
